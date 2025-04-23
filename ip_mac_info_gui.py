import tkinter as tk
import socket
import uuid
import subprocess


class NetworkInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('网络信息查看器')
        self.root.geometry('400x300')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.info_frame = tk.Frame(root)
        self.info_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.qq_label = tk.Label(self.info_frame, text='qq 510415364')
        self.qq_label.grid(row=0, column=0, sticky='w', pady=5)

        self.ip_label = tk.Label(self.info_frame, text='IP地址: ')
        self.ip_label.grid(row=1, column=0, sticky='w', pady=5)

        self.mac_label = tk.Label(self.info_frame, text='MAC地址: ')
        self.mac_label.grid(row=1, column=0, sticky='w', pady=5)

        self.mask_label = tk.Label(self.info_frame, text='子网掩码: ')
        self.mask_label.grid(row=2, column=0, sticky='w', pady=5)

        self.ipconfig_label = tk.Label(self.info_frame, text='ipconfig /all 信息: ')
        self.ipconfig_label.grid(row=3, column=0, sticky='w', pady=5)
        self.root.geometry('')
        self.ipconfig_text = tk.Text(self.info_frame, height=20, width=60)
        scrollbar = tk.Scrollbar(self.info_frame, command=self.ipconfig_text.yview)
        self.ipconfig_text.configure(yscrollcommand=scrollbar.set)
        self.ipconfig_text.grid(row=4, column=0, sticky='nsew')
        scrollbar.grid(row=4, column=1, sticky='ns')

        self.close_button = tk.Button(self.info_frame, text='关闭', command=self.root.destroy)
        self.close_button.grid(row=5, column=0, pady=10)

        self.update_info()

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f'获取IP地址失败: {e}')
            return '未知'

    def get_mac_address(self):
        try:
            mac = uuid.getnode()
            mac = ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))
            return mac
        except Exception as e:
            print(f'获取MAC地址失败: {e}')
            return '未知'

    def get_subnet_mask(self):
        try:
            import subprocess
            import sys
            if sys.platform.startswith('win'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, check=True, startupinfo=startupinfo if sys.platform.startswith('win') else None)
            output = result.stdout
            import re
            # 修改正则表达式以提高匹配准确性
            match = re.search(r'子网掩码[ ]*: ?([0-9.]+)|Subnet[ ]*Mask[ ]*: ?([0-9.]+)', output, re.IGNORECASE)
            if match:
                return match.group(1) or match.group(2)
            else:
                print('未找到子网掩码信息。')
                return '未知'
        except subprocess.CalledProcessError as e:
            print(f'执行 ipconfig 命令失败: {e}')
            return '未知'
        except Exception as e:
            print(f'获取子网掩码时发生未知错误: {e}')
            return '未知'

    def get_ipconfig_all(self):
        try:
            import subprocess
            import sys
            if sys.platform.startswith('win'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, check=True, startupinfo=startupinfo if sys.platform.startswith('win') else None)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f'执行 ipconfig /all 命令失败: {e}')
            return '执行命令失败'

    def update_info(self):
        ip = self.get_ip_address()
        mac = self.get_mac_address()
        mask = self.get_subnet_mask()
        ipconfig_info = self.get_ipconfig_all()

        self.ip_label.config(text=f'IP地址: {ip}')
        self.mac_label.config(text=f'MAC地址: {mac}')
        self.mask_label.config(text=f'子网掩码: {mask}')
        self.ipconfig_text.delete(1.0, tk.END)
        self.ipconfig_text.insert(tk.END, ipconfig_info)


if __name__ == '__main__':
    root = tk.Tk()
    app = NetworkInfoApp(root)
    root.mainloop()
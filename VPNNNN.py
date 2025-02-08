import os
import subprocess
import time
import requests
import keyboard

# Путь к исполняемому файлу OpenVPN
openvpn_path = r"D:\OpenVPN\bin\openvpn.exe"

# Путь к конфигурационным файлам OpenVPN
vpn_configs = [
    r"D:\OpenVPN\config\vpn1.ovpn",
    r"D:\OpenVPN\config\vpn2.ovpn",
    r"C:\OpenVPN\config\vpn3.ovpn"
]

current_vpn_process = None
current_vpn_config = None

def connect_to_vpn(vpn_config):
    global current_vpn_process, current_vpn_config
    print(f"Подключение к {vpn_config}...")
    current_vpn_process = subprocess.Popen([openvpn_path, "--config", vpn_config])
    current_vpn_config = vpn_config
    time.sleep(10)  # Ждать некоторое время, чтобы соединение установилось

def disconnect_from_vpn():
    global current_vpn_process, current_vpn_config
    if current_vpn_process:
        print("Отключение от VPN...")
        current_vpn_process.terminate()
        current_vpn_process = None
        current_vpn_config = None
        time.sleep(5)  # Дождаться завершения процесса отключения

def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Не удалось получить IP"
    except Exception as e:
        return f"Ошибка при получении IP: {e}"

def toggle_vpn():
    global current_vpn_process, current_vpn_config
    if current_vpn_process is None:
        if vpn_configs:
            connect_to_vpn(vpn_configs[0])
            current_ip = get_current_ip()
            print(f"Текущий IP-адрес: {current_ip}")
    else:
        disconnect_from_vpn()

def main():
    print("Ожидание нажатия клавиши 'U' для подключения/отключения к VPN...")
    keyboard.add_hotkey('u', toggle_vpn)
    keyboard.wait()

if __name__ == "__main__":
    main()

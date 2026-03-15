import subprocess
import psutil
import os 
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False





def get_all_processes():
    processes = []
    username = os.getlogin()
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            # Получаем информацию о пользователе и ПУТЬ к файлу
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'exe'])
            
            if pinfo['username'] and username in pinfo['username'] and pinfo['exe']:
                processes.append(pinfo)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    processes.sort(key=lambda x: x["name"])
    # for p in processes:
    #     print(p)
    return processes

def check_block_status(proc_name):
    cmd = f'netsh advfirewall firewall show rule name=Block_{proc_name}'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp866')
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке статуса блокировки: {e}")
        return False
    
    
def set_strict_block(proc_path, rule_name):
    # Блокируем и исходящий, и входящий трафик для всех профилей (Общий, Частный, Доменный)
    commands = [
        f'netsh advfirewall firewall add rule name="{rule_name}_OUT" dir=out action=block program="{proc_path}" enable=yes profile=any',
        f'netsh advfirewall firewall add rule name="{rule_name}_IN" dir=in action=block program="{proc_path}" enable=yes profile=any'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, capture_output=True)



def set_traffic_block(proc_path, rule_name, block=True):
    """
    block=True  -> Создает правило блокировки
    block=False -> Удаляет правило (разблокирует)
    """
    if block:
        # Команда добавляет правило для блокировки исходящего (out) трафика
        # Можно добавить вторую такую же для 'dir=in' (входящий)
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block program="{proc_path}" enable=yes'
    else:
        # Удаляем все правила с этим именем
        cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
    
    try:
        # Запускаем команду скрыто
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp866')
        if result.returncode == 0:
            return True, "Успешно"
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)
    
    
def main():
    # print(get_all_processes())
    print(check_block_status(r"C:\Users\stormcage\AppData\Local\Discord\app-1.0.9228\Discord.exe"))
    # print(set_traffic_block(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "Block brave", block=False))

    return    

if __name__ == "__main__":
    if is_admin():
        # get_blocked_programs()
        print(check_block_status("Discord.exe"))
        # main()
        sys.exit(0)
    else:
        print("!!! ОШИБКА: Запустите от имени АДМИНИСТРАТОРА !!!")
        sys.exit(1)
    
    

    
    

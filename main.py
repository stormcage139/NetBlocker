import subprocess
import psutil
import os 
import ctypes, sys
import platform
import getpass



def is_admin():
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0


def get_all_processes():
    processes = []
    username = getpass.getuser()
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
    if platform.system() == 'Windows':
        cmd = f'netsh advfirewall firewall show rule name=Block_{proc_name}'
        encoding = 'cp866'
    else:
        # На Linux проверяем iptables по комментарию
        cmd = f'iptables -L OUTPUT -n | grep "Block_{proc_name}"'
        encoding = 'utf-8'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding)
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
    if platform.system() == 'Windows':
        if block:
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block program="{proc_path}" enable=yes'
        else:
            cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        encoding = 'cp866'
    else:
        # На Linux: найти UID процесса по пути exe
        uid = None
        for proc in psutil.process_iter(['exe', 'uids']):
            if proc.info['exe'] == proc_path:
                uid = proc.info['uids'].real
                break
        if uid is None:
            return False, "Процесс не найден или не имеет UID"
        if block:
            cmd = f'iptables -A OUTPUT -m owner --uid-owner {uid} -j DROP -m comment --comment "{rule_name}"'
        else:
            cmd = f'iptables -D OUTPUT -m owner --uid-owner {uid} -j DROP -m comment --comment "{rule_name}"'
        encoding = 'utf-8'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding)
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

def get_all_blocked_rules():
    if platform.system() == 'Windows':
        cmd = 'netsh advfirewall firewall show rule name=all'
        encoding = 'cp866'
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding)
            if result.returncode == 0:
                lines = result.stdout.split("-" * 70)
                blocked_rules = {}
                for line in lines:
                    if 'Rule Name:' in line and 'Block_' in line:
                        rule_name = line.split(':', 1)[1].strip()
                        blocked_rules[rule_name] = True
                return blocked_rules
            else:
                return {}
        except Exception as e:
            print(f"Ошибка при получении правил: {e}")
            return {}
    else:
        # На Linux: парсим iptables
        cmd = 'iptables -L OUTPUT -n'
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                blocked_rules = {}
                for line in result.stdout.split('\n'):
                    if 'Block_' in line:
                        # Ищем комментарий /* Block_<name> */
                        if '/*' in line and '*/' in line:
                            comment = line.split('/*')[1].split('*/')[0]
                            if comment.startswith('Block_'):
                                blocked_rules[comment] = True
                return blocked_rules
            else:
                return {}
        except Exception as e:
            print(f"Ошибка при получении правил: {e}")
            return {}

if __name__ == "__main__":
    if is_admin():
        # get_blocked_programs()
        print(check_block_status("Discord.exe"))
        # main()
        sys.exit(0)
    else:
        print(get_all_blocked_rules())
        print("!!! ОШИБКА: Запустите от имени АДМИНИСТРАТОРА !!!")
        sys.exit(1)
    
    

    
    

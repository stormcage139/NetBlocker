import subprocess

def get_all_blocked_rules():
    cmd = 'netsh advfirewall firewall show rule name=all'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
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

def main():
    print(get_all_blocked_rules())
    return
    
if __name__ == "__main__":
    main()
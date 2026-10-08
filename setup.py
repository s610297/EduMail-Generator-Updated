import subprocess
import sys

######## This script is only for educational purpose ########
######## use it on your own RISK ########
######## I'm not responsible for any loss or damage ########
######## caused to you using this script ########
######## Github Repo - https://git.io/JJisT/ ########

def install(name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])

def main():
    # Updated packages for Selenium 4
    my_packages = [
        'requests',
        'faker',
        'selenium>=4.0.0',
        'colorama',
        'webdriver-manager'
    ]

    print('[*] Installing required packages...\n')
    
    for package in my_packages:
        try:
            print(f'[*] Installing {package}...')
            install(package)
            print(f'[✓] {package} installed successfully\n')
        except Exception as e:
            print(f'[✗] Error installing {package}: {str(e)}\n')
            continue

    print('\n[✓] Setup Completed Successfully!')
    print('[*] All drivers will be automatically managed by webdriver-manager')
    print('[*] You can now run: python bot.py\n')

if __name__ == '__main__':
    main()

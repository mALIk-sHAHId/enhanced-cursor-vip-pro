# main.py
# This script allows the user to choose which script to run.
import os
import sys
import json
from logo import print_logo, version
from colorama import Fore, Style, init
import locale
import platform
import requests
import subprocess
from config import get_config  
import argparse  # Add this import at the top

# Only import windll on Windows systems
if platform.system() == 'Windows':
    import ctypes
    # 只在 Windows 上导入 windll
    from ctypes import windll

# Initialize colorama
init()

# Define emoji and color constants
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "MENU": "📋",
    "ARROW": "➜",
    "LANG": "🌐",
    "UPDATE": "🔄",
    "ADMIN": "🔐"
}

# Function to check if running as frozen executable
def is_frozen():
    """Check if the script is running as a frozen executable."""
    return getattr(sys, 'frozen', False)

# Function to check admin privileges (Windows only)
def is_admin():
    """Check if the script is running with admin privileges (Windows only)."""
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    # Always return True for non-Windows to avoid changing behavior
    return True

# Function to restart with admin privileges
def run_as_admin():
    """Restart the current script with admin privileges (Windows only)."""
    if platform.system() != 'Windows':
        return False
        
    try:
        args = [sys.executable] + sys.argv
        
        # Request elevation via ShellExecute
        print(f"{Fore.YELLOW}{EMOJI['ADMIN']} Requesting administrator privileges...{Style.RESET_ALL}")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", args[0], " ".join('"' + arg + '"' for arg in args[1:]), None, 1)
        return True
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to restart with admin privileges: {e}{Style.RESET_ALL}")
        return False

class Translator:
    def __init__(self):
        self.translations = {}
        self.current_language = self.detect_system_language()  # Use correct method name
        self.fallback_language = 'en'  # Fallback language if translation is missing
        self.load_translations()
    
    def detect_system_language(self):
        """Detect system language and return corresponding language code"""
        try:
            system = platform.system()
            
            if system == 'Windows':
                return self._detect_windows_language()
            else:
                return self._detect_unix_language()
                
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Failed to detect system language: {e}{Style.RESET_ALL}")
            return 'en'
    
    def _detect_windows_language(self):
        """Detect language on Windows systems"""
        try:
            # Ensure we are on Windows
            if platform.system() != 'Windows':
                return 'en'
                
            # Get keyboard layout
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            threadid = user32.GetWindowThreadProcessId(hwnd, 0)
            layout_id = user32.GetKeyboardLayout(threadid) & 0xFFFF
            
            # Map language ID to our language codes
            language_map = {
                0x0409: 'en',      # English
                0x0404: 'zh_tw',   # Traditional Chinese
                0x0804: 'zh_cn',   # Simplified Chinese
            }
            
            return language_map.get(layout_id, 'en')
        except:
            return self._detect_unix_language()
    
    def _detect_unix_language(self):
        """Detect language on Unix-like systems (Linux, macOS)"""
        try:
            # Get the system locale
            system_locale = locale.getdefaultlocale()[0]
            if not system_locale:
                return 'en'
            
            system_locale = system_locale.lower()
            
            # Map locale to our language codes
            if system_locale.startswith('zh_tw') or system_locale.startswith('zh_hk'):
                return 'zh_tw'
            elif system_locale.startswith('zh_cn'):
                return 'zh_cn'
            elif system_locale.startswith('en'):
                return 'en'
            
            # Try to get language from LANG environment variable as fallback
            env_lang = os.getenv('LANG', '').lower()
            if 'tw' in env_lang or 'hk' in env_lang:
                return 'zh_tw'
            elif 'cn' in env_lang:
                return 'zh_cn'
            
            return 'en'
        except:
            return 'en'
    
    def load_translations(self):
        """Load all available translations"""
        try:
            locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
            if hasattr(sys, '_MEIPASS'):
                locales_dir = os.path.join(sys._MEIPASS, 'locales')
            
            if not os.path.exists(locales_dir):
                print(f"{Fore.RED}{EMOJI['ERROR']} Locales directory not found{Style.RESET_ALL}")
                return

            for file in os.listdir(locales_dir):
                if file.endswith('.json'):
                    lang_code = file[:-5]  # Remove .json
                    try:
                        with open(os.path.join(locales_dir, file), 'r', encoding='utf-8') as f:
                            self.translations[lang_code] = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        print(f"{Fore.RED}{EMOJI['ERROR']} Error loading {file}: {e}{Style.RESET_ALL}")
                        continue
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to load translations: {e}{Style.RESET_ALL}")
    
    def get(self, key, **kwargs):
        """Get translated text with fallback support"""
        try:
            # Try current language
            result = self._get_translation(self.current_language, key)
            if result == key and self.current_language != self.fallback_language:
                # Try fallback language if translation not found
                result = self._get_translation(self.fallback_language, key)
            return result.format(**kwargs) if kwargs else result
        except Exception:
            return key
    
    def _get_translation(self, lang_code, key):
        """Get translation for a specific language"""
        try:
            keys = key.split('.')
            value = self.translations.get(lang_code, {})
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, key)
                else:
                    return key
            return value
        except Exception:
            return key
    
    def set_language(self, lang_code):
        """Set current language with validation"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())

# Create translator instance
translator = Translator()

def get_input(prompt, choices=None):
    """Get user input with proper formatting."""
    if choices:
        prompt = f"{prompt} ({choices})"
    return input(f"{Fore.CYAN}{EMOJI['ARROW']} {prompt}{Style.RESET_ALL}: ").strip()

def print_menu():
    """Print the main menu."""
    menu_width = 60  # Slightly increased width for better spacing
    
    def get_display_length(text):
        """Calculate the display length of text, accounting for special characters"""
        # Count emoji and special characters as 2 spaces
        emoji_chars = '✅🌟⭐❌🌐🔥🚀'
        length = len(text)
        for char in text:
            if char in emoji_chars:
                length += 1  # Add extra space for emoji width
        return length
    
    def get_padding(text):
        display_length = get_display_length(text)
        return menu_width - display_length - 2  # -2 for the left and right borders
    
    print(f"\n{Fore.CYAN}╭{'─' * menu_width}╮{Style.RESET_ALL}")
    
    # Menu items with their colors
    menu_items = [
        (f" 1. ✅ Reset Machine ID", Fore.CYAN),
        (f" 2. ✅ Register New Cursor Account", Fore.CYAN),
        (f" 3. 🌟 Register with Google Account", Fore.CYAN),
        (f"    ┗━━ 🔥 LIFETIME ACCESS ENABLED 🔥", Fore.YELLOW),
        (f" 4. ⭐ Register with GitHub Account", Fore.CYAN),
        (f"    ┗━━ 🚀 LIFETIME ACCESS ENABLED 🚀", Fore.YELLOW),
        (f" 5. ✅ Manual Register", Fore.CYAN),
        (f" 6. ✅ Quit Cursor", Fore.CYAN),
        (f" 7. ✅ Disable Auto Update", Fore.CYAN),
        (f" 8. 🌐 Change Language", Fore.CYAN),
        (f" 9. ❌ Exit", Fore.CYAN)
    ]
    
    for text, color in menu_items:
        padding = ' ' * get_padding(text)
        print(f"{color}│{Style.RESET_ALL}{text}{padding}{color}│{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}╰{'─' * menu_width}╯{Style.RESET_ALL}")
    print()

def select_language():
    """Language selection menu"""
    print(f"\n{Fore.CYAN}{EMOJI['LANG']} {translator.get('menu.select_language')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")
    
    languages = translator.get_available_languages()
    for i, lang in enumerate(languages):
        lang_name = translator.get(f"languages.{lang}")
        print(f"{Fore.GREEN}{i}{Style.RESET_ALL}. {lang_name}")
    
    try:
        choice = input(f"\n{EMOJI['ARROW']} {Fore.CYAN}{translator.get('menu.input_choice', choices=f'0-{len(languages)-1}')}: {Style.RESET_ALL}")
        if choice.isdigit() and 0 <= int(choice) < len(languages):
            translator.set_language(languages[int(choice)])
            return True
        else:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
            return False
    except (ValueError, IndexError):
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
        return False

def check_latest_version():
    """Check if current version matches the latest release version"""
    try:
        print(f"\n{Fore.CYAN}{EMOJI['UPDATE']} {translator.get('updater.checking')}{Style.RESET_ALL}")
        
        # Get latest version from GitHub API with timeout and proper headers
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'CursorFreeVIP-Updater'
        }
        response = requests.get(
            "https://api.github.com/repos/mALIk-sHAHId/enhanced-cursor-vip-pro/releases/latest",
            headers=headers,
            timeout=10
        )
        
        # Check if response is successful
        if response.status_code != 200:
            raise Exception(f"GitHub API returned status code {response.status_code}")
            
        response_data = response.json()
        if "tag_name" not in response_data:
            raise Exception("No version tag found in GitHub response")
            
        latest_version = response_data["tag_name"].lstrip('v')
        
        # Validate version format
        if not latest_version:
            raise Exception("Invalid version format received")
        
        if latest_version != version:
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.new_version_available', current=version, latest=latest_version)}{Style.RESET_ALL}")
            
            # Ask user if they want to update
            while True:
                choice = input(f"\n{EMOJI['ARROW']} {Fore.CYAN}{translator.get('updater.update_confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()
                if choice in ['', 'y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.update_skipped')}{Style.RESET_ALL}")
                    return
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
            
            try:
                # Execute update command based on platform
                if platform.system() == 'Windows':
                    update_command = 'irm https://raw.githubusercontent.com/mALIk-sHAHId/enhanced-cursor-vip-pro/main/scripts/install.ps1 | iex'
                    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', update_command], check=True)
                else:
                    # For Linux/Mac, download and execute the install script
                    install_script_url = 'https://raw.githubusercontent.com/mALIk-sHAHId/enhanced-cursor-vip-pro/main/scripts/install.sh'
                    
                    # First verify the script exists
                    script_response = requests.get(install_script_url, timeout=5)
                    if script_response.status_code != 200:
                        raise Exception("Installation script not found")
                        
                    # Save and execute the script
                    with open('install.sh', 'wb') as f:
                        f.write(script_response.content)
                    
                    os.chmod('install.sh', 0o755)  # Make executable
                    subprocess.run(['./install.sh'], check=True)
                    
                    # Clean up
                    if os.path.exists('install.sh'):
                        os.remove('install.sh')
                
                print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.updating')}{Style.RESET_ALL}")
                sys.exit(0)
                
            except Exception as update_error:
                print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.update_failed', error=str(update_error))}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.manual_update_required')}{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.up_to_date')}{Style.RESET_ALL}")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.network_error', error=str(e))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.continue_anyway')}{Style.RESET_ALL}")
        return
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.check_failed', error=str(e))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.continue_anyway')}{Style.RESET_ALL}")
        return

def handle_auth():
    """Handle automatic authentication"""
    try:
        from oauth_auth import main as oauth_main
        return oauth_main("google", translator)
    except Exception as e:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} {str(e)}{Style.RESET_ALL}")
        return False

def handle_menu_action(choice):
    """Handle menu selection and return True if action was successful"""
    try:
        if choice == "1":
            from reset_machine_manual import main as reset_main
            return reset_main(translator)
        elif choice == "2":
            from cursor_register import main as register_main
            return register_main(translator)
        elif choice == "3":
            from oauth_auth import main as oauth_main
            return oauth_main("google", translator)
        elif choice == "4":
            from oauth_auth import main as oauth_main
            return oauth_main("github", translator)
        elif choice == "5":
            from cursor_register_manual import main as register_manual_main
            return register_manual_main(translator)
        elif choice == "6":
            from quit_cursor import main as quit_main
            return quit_main(translator)
        elif choice == "7":
            from disable_auto_update import main as disable_update_main
            return disable_update_main(translator)
        elif choice == "8":
            return select_language()
        elif choice == "9":
            print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('main.goodbye')}{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('main.invalid_choice')}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} {str(e)}{Style.RESET_ALL}")
        return False

def modify_cursor_ui():
    """Modify Cursor UI to remove upgrade prompts and set custom button."""
    try:
        from reset_machine_manual import get_workbench_cursor_path, modify_workbench_js
        workbench_path = get_workbench_cursor_path(translator)
        modify_workbench_js(workbench_path, translator)
    except:
        pass

def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Cursor VIP Reset Master')
    parser.add_argument('-auth', action='store_true', help='Automatically run Google authentication')
    args = parser.parse_args()

    is_windows = platform.system() == 'Windows'
    needs_admin = False

    # Modify Cursor UI at startup silently
    modify_cursor_ui()

    # If -auth flag is provided, run authentication directly
    if args.auth:
        handle_auth()
        sys.exit(0)

    while True:
        print_logo()
        print_menu()
        
        try:
            choice = get_input(translator.get('menu.input_choice', choices="1-9"))
            
            if not choice.strip():
                continue

            # Check if the selected option needs admin rights
            if is_windows and choice in ['1', '7']:  # Reset Machine ID or Disable Auto Update
                if not is_admin():
                    print(f"\n{Fore.YELLOW}{EMOJI['ADMIN']} {translator.get('admin.required')}")
                    print(f"{Fore.YELLOW}{translator.get('admin.restart_prompt')}{Style.RESET_ALL}")
                    confirm = get_input(translator.get('admin.restart_confirm')).lower()
                    if confirm in ['y', 'yes']:
                        if run_as_admin():
                            sys.exit()
                    else:
                        print(f"{Fore.YELLOW}{translator.get('admin.continue_warning')}{Style.RESET_ALL}")
                        get_input(translator.get('admin.press_continue'))
                        continue
            
            # Handle the menu action
            success = handle_menu_action(choice)
            
            # Only show "press enter" if the action was successful and we're not exiting
            if success and choice != "9":
                get_input(translator.get('main.press_continue'))

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 {translator.get('main.goodbye')}{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}{EMOJI['ERROR']} {str(e)}{Style.RESET_ALL}")
            get_input(translator.get('main.press_continue'))

if __name__ == "__main__":
    main()
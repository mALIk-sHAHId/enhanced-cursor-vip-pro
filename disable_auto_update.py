import os
import sys
import platform
import shutil
from colorama import Fore, Style, init
import subprocess
from config import get_config

# Initialize colorama
init()

# Define emoji constants
EMOJI = {
    "PROCESS": "🔄",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "FOLDER": "📁",
    "FILE": "📄",
    "STOP": "🛑",
    "CHECK": "✔️"
}

class AutoUpdateDisabler:
    def __init__(self, translator=None):
        self.translator = translator
        self.system = platform.system()
        
        # Get path from configuration file
        config = get_config(translator)
        if config:
            if self.system == "Windows":
                self.updater_path = config.get('WindowsPaths', 'updater_path', fallback=os.path.join(os.getenv("LOCALAPPDATA", ""), "cursor-updater"))
            elif self.system == "Darwin":
                self.updater_path = config.get('MacPaths', 'updater_path', fallback=os.path.expanduser("~/Library/Application Support/cursor-updater"))
            elif self.system == "Linux":
                self.updater_path = config.get('LinuxPaths', 'updater_path', fallback=os.path.expanduser("~/.config/cursor-updater"))
        else:
            # If configuration loading fails, use default paths
            self.updater_paths = {
                "Windows": os.path.join(os.getenv("LOCALAPPDATA", ""), "cursor-updater"),
                "Darwin": os.path.expanduser("~/Library/Application Support/cursor-updater"),
                "Linux": os.path.expanduser("~/.config/cursor-updater")
            }
            self.updater_path = self.updater_paths.get(self.system)

    def _kill_cursor_processes(self):
        """End all Cursor processes"""
        try:
            print(f"{Fore.CYAN}{EMOJI['PROCESS']} {self.translator.get('update.killing_processes') if self.translator else '正在结束 Cursor 进程...'}{Style.RESET_ALL}")
            
            if self.system == "Windows":
                subprocess.run(['taskkill', '/F', '/IM', 'Cursor.exe', '/T'], capture_output=True)
            else:
                subprocess.run(['pkill', '-f', 'Cursor'], capture_output=True)
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('update.processes_killed') if self.translator else 'Cursor 进程已结束'}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('update.kill_process_failed', error=str(e)) if self.translator else f'结束进程失败: {e}'}{Style.RESET_ALL}")
            return False

    def _remove_updater_directory(self):
        """Delete updater directory"""
        try:
            updater_path = self.updater_path
            if not updater_path:
                raise OSError(self.translator.get('update.unsupported_os', system=self.system) if self.translator else f"不支持的操作系统: {self.system}")

            print(f"{Fore.CYAN}{EMOJI['FOLDER']} {self.translator.get('update.removing_directory') if self.translator else '正在删除更新程序目录...'}{Style.RESET_ALL}")
            
            if os.path.exists(updater_path):
                if os.path.isdir(updater_path):
                    shutil.rmtree(updater_path)
                else:
                    os.remove(updater_path)
                    
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('update.directory_removed') if self.translator else '更新程序目录已删除'}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('update.remove_directory_failed', error=str(e)) if self.translator else f'删除目录失败: {e}'}{Style.RESET_ALL}")
            return False

    def _create_blocking_file(self):
        """Create blocking file"""
        try:
            updater_path = self.updater_path
            if not updater_path:
                raise OSError(self.translator.get('update.unsupported_os', system=self.system) if self.translator else f"不支持的操作系统: {self.system}")

            print(f"{Fore.CYAN}{EMOJI['FILE']} {self.translator.get('update.creating_block_file') if self.translator else '正在创建阻止文件...'}{Style.RESET_ALL}")
            
            # Create empty file
            open(updater_path, 'w').close()
            
            # Set read-only attribute
            if self.system == "Windows":
                os.system(f'attrib +r "{updater_path}"')
            else:
                os.chmod(updater_path, 0o444)  # Set to read-only
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('update.block_file_created') if self.translator else '阻止文件已创建'}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('update.create_block_file_failed', error=str(e)) if self.translator else f'创建阻止文件失败: {e}'}{Style.RESET_ALL}")
            return False

    def disable_auto_update(self):
        """Disable auto update"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('update.start_disable') if self.translator else '开始禁用自动更新...'}{Style.RESET_ALL}")
            
            # 1. End processes
            if not self._kill_cursor_processes():
                return False
                
            # 2. Delete directory
            if not self._remove_updater_directory():
                return False
                
            # 3. Create blocking file
            if not self._create_blocking_file():
                return False
                
            print(f"{Fore.GREEN}{EMOJI['CHECK']} {self.translator.get('update.disable_success') if self.translator else '自动更新已禁用'}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('update.disable_failed', error=str(e)) if self.translator else f'禁用自动更新失败: {e}'}{Style.RESET_ALL}")
            return False

def run(translator=None):
    """Convenient function for directly calling the disable function"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['STOP']} {translator.get('update.title') if translator else 'Disable Cursor Auto Update'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    disabler = AutoUpdateDisabler(translator)
    disabler.disable_auto_update()

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('update.press_enter') if translator else 'Press Enter to Continue...'}")

if __name__ == "__main__":
    from main import translator as main_translator
    run(main_translator) 
from colorama import Fore, Style, init, Back
from dotenv import load_dotenv
import os
import platform

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Build the full path to the .env file
env_path = os.path.join(current_dir, '.env')

# Load environment variables, specifying the .env file path
load_dotenv(env_path)
# Get the version number, using the default value if not found
version = os.getenv('VERSION', '1.0.0')

# Initialize colorama
init(autoreset=True)  # Add autoreset to prevent color bleeding

def get_terminal_width():
    """Get terminal width or return default 80."""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def center_text(text, width=None):
    """Center text based on terminal width."""
    if width is None:
        width = get_terminal_width()
    return text.center(width)

CURSOR_LOGO = f"""{Fore.CYAN}
    ██████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ 
   ██╔════╝██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗
   ██║     ██║   ██║██████╔╝███████╗██║   ██║██████╔╝
   ██║     ██║   ██║██╔══██╗╚════██║██║   ██║██╔══██╗
   ╚██████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║
    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝{Fore.WHITE}
   ╔{'═' * 47}╗
   ║{Fore.RED + Style.BRIGHT + Back.BLACK}                    RESET MASTER                    {Fore.WHITE + Style.NORMAL + Back.BLACK}║
   ╚{'═' * 47}╝{Fore.YELLOW}
           🔄 Advanced VIP Reset Tool v{version} 🔄{Style.BRIGHT}{Fore.GREEN}
             Author: CodeCrafts | mALIk-sHAHId
    ═══════════════════════════════════════════════════
    Github: https://github.com/mALIk-sHAHId/enhanced-cursor-vip-pro{Fore.CYAN}
    ╭{'─' * 46}╮
    │{Style.NORMAL}     Press 8 to change language | 按下 8 键切换语言     {Fore.CYAN}│
    ╰{'─' * 46}╯{Style.RESET_ALL}"""

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

def print_logo():
    """Print the logo with proper screen clearing and centering."""
    clear_screen()
    print(CURSOR_LOGO)

if __name__ == "__main__":
    print_logo()
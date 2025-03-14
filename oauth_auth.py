import os
from colorama import Fore, Style, init
import time
import random
import webbrowser
import sys
import json
from DrissionPage import ChromiumPage, ChromiumOptions
from cursor_auth import CursorAuth
from utils import get_random_wait_time, get_default_chrome_path
from config import get_config

# Initialize colorama
init()

# Define emoji constants
EMOJI = {
    'START': '🚀',
    'OAUTH': '🔑',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'WAIT': '⏳',
    'INFO': 'ℹ️'
}

class OAuthHandler:
    def __init__(self, translator=None):
        self.translator = translator
        self.config = get_config(translator)
        os.environ['BROWSER_HEADLESS'] = 'False'
        self.browser = None
        
    def _get_active_profile(self, user_data_dir):
        """Find the existing default/active Chrome profile"""
        try:
            # List all profile directories
            profiles = []
            for item in os.listdir(user_data_dir):
                if item == 'Default' or (item.startswith('Profile ') and os.path.isdir(os.path.join(user_data_dir, item))):
                    profiles.append(item)
            
            if not profiles:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} No Chrome profiles found, using Default{Style.RESET_ALL}")
                return 'Default'
            
            # First check if Default profile exists
            if 'Default' in profiles:
                print(f"{Fore.CYAN}{EMOJI['INFO']} Found Default Chrome profile{Style.RESET_ALL}")
                return 'Default'
            
            # If no Default profile, check Local State for last used profile
            local_state_path = os.path.join(user_data_dir, 'Local State')
            if os.path.exists(local_state_path):
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
                
                # Get info about last used profile
                profile_info = local_state.get('profile', {})
                last_used = profile_info.get('last_used', '')
                info_cache = profile_info.get('info_cache', {})
                
                # Try to find an active profile
                for profile in profiles:
                    profile_path = profile.replace('\\', '/')
                    if profile_path in info_cache:
                        #print(f"{Fore.CYAN}{EMOJI['INFO']} Using existing Chrome profile: {profile}{Style.RESET_ALL}")
                        return profile
            
            # If no profile found in Local State, use the first available profile
            print(f"{Fore.CYAN}{EMOJI['INFO']} Using first available Chrome profile: {profiles[0]}{Style.RESET_ALL}")
            return profiles[0]
            
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Error finding Chrome profile, using Default: {str(e)}{Style.RESET_ALL}")
            return 'Default'
        
    def setup_browser(self):
        """Setup browser for OAuth flow using active profile"""
        try:
            # Kill any existing Chrome processes
            if os.name == 'nt':  # Windows
                os.system('taskkill /f /im chrome.exe >nul 2>&1')
            else:  # Linux/Mac
                os.system('pkill -f chrome >/dev/null 2>&1')
            
            time.sleep(1)  # Wait for Chrome to close
            
            # Get the default Chrome user data directory
            if os.name == 'nt':  # Windows
                user_data_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
            elif os.name == 'posix':  # macOS/Linux
                if sys.platform == 'darwin':  # macOS
                    user_data_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')
                else:  # Linux
                    user_data_dir = os.path.expanduser('~/.config/google-chrome')
            
            # Get active profile
            active_profile = self._get_active_profile(user_data_dir)
            
            # Set Chrome options
            chrome_path = get_default_chrome_path()
            
            print(f"{Fore.CYAN}{EMOJI['INFO']} Opening Chrome Please Wait...{Style.RESET_ALL}")
            
            # Create browser instance with basic configuration
            co = ChromiumOptions()
            co.set_paths(browser_path=chrome_path, user_data_path=user_data_dir)
            co.set_argument(f'--profile-directory={active_profile}')
            co.set_argument('--no-first-run')
            co.set_argument('--no-default-browser-check')
            
            self.browser = ChromiumPage(co)
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Browser setup failed: {str(e)}{Style.RESET_ALL}")
            return False

    def handle_google_auth(self):
        """Handle Google OAuth authentication"""
        return self._handle_oauth("google")
        
    def handle_github_auth(self):
        """Handle GitHub OAuth authentication"""
        return self._handle_oauth("github")
        
    def _handle_oauth(self, auth_type):
        """Handle OAuth authentication for both Google and GitHub
        
        Args:
            auth_type (str): Type of authentication ('google' or 'github')
        """
        try:
            if not self.setup_browser():
                return False, None
                
            # Navigate to auth URL
            self.browser.get("https://authenticator.cursor.sh/sign-up")
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # Set selectors based on auth type
            if auth_type == "google":
                selectors = [
                    "//a[@class='rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button auth-method-button_AuthMethodButton__irESX'][contains(@href,'GoogleOAuth')]",
                    "(//a[@class='rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button auth-method-button_AuthMethodButton__irESX'])[1]"
                ]
            else:  # github
                selectors = [
                    "(//a[@class='rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button auth-method-button_AuthMethodButton__irESX'])[2]"
                ]
            
            # Wait for the button to be available
            auth_btn = None
            max_button_wait = 30  # 30 seconds
            button_start_time = time.time()
            
            while time.time() - button_start_time < max_button_wait:
                for selector in selectors:
                    try:
                        auth_btn = self.browser.ele(f"xpath:{selector}", timeout=1)
                        if auth_btn and auth_btn.is_displayed():
                            break
                    except:
                        continue
                if auth_btn:
                    break
                time.sleep(1)
            
            if auth_btn:
                # Click the button and wait for page load
                auth_btn.click()
                time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                
                # Check if we're on account selection page
                if auth_type == "google" and "accounts.google.com" in self.browser.url:
                    alert_js = """
                    alert('Please select your Google account manually to continue with Cursor authentication');
                    """
                    try:
                        self.browser.run_js(alert_js)
                    except Exception as e:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Alert display failed: {str(e)}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{EMOJI['INFO']} Please select your Google account manually to continue with Cursor authentication...{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}{EMOJI['INFO']} Waiting for authentication to complete...{Style.RESET_ALL}")
                
                # Wait for authentication to complete
                max_wait = 300  # 5 minutes
                start_time = time.time()
                last_url = self.browser.url
                
                print(f"{Fore.CYAN}{EMOJI['WAIT']} Checking authentication status...{Style.RESET_ALL}")
                
                while time.time() - start_time < max_wait:
                    try:
                        # Check for authentication cookies
                        cookies = self.browser.cookies()
                        
                        for cookie in cookies:
                            if cookie.get("name") == "WorkosCursorSessionToken":
                                value = cookie.get("value", "")
                                if "::" in value:
                                    token = value.split("::")[-1]
                                elif "%3A%3A" in value:
                                    token = value.split("%3A%3A")[-1]
                                
                                if token:
                                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Authentication successful!{Style.RESET_ALL}")
                                    # Navigate to settings page
                                    print(f"{Fore.CYAN}{EMOJI['INFO']} Navigating to settings page...{Style.RESET_ALL}")
                                    self.browser.get("https://www.cursor.com/settings")
                                    time.sleep(3)  # Wait for settings page to load
                                    
                                    # Get email from settings page
                                    try:
                                        email_element = self.browser.ele("css:div[class='flex w-full flex-col gap-2'] div:nth-child(2) p:nth-child(2)")
                                        if email_element:
                                            actual_email = email_element.text
                                            print(f"{Fore.CYAN}{EMOJI['INFO']} Found email: {actual_email}{Style.RESET_ALL}")
                                    except Exception as e:
                                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Could not find email: {str(e)}{Style.RESET_ALL}")
                                        actual_email = "user@cursor.sh"
                                    
                                    # Check usage count
                                    try:
                                        usage_element = self.browser.ele("css:div[class='flex flex-col gap-4 lg:flex-row'] div:nth-child(1) div:nth-child(1) span:nth-child(2)")
                                        if usage_element:
                                            usage_text = usage_element.text
                                            print(f"{Fore.CYAN}{EMOJI['INFO']} Usage count: {usage_text}{Style.RESET_ALL}")
                                            
                                            # Check if account is expired
                                            if usage_text.strip() == "150 / 150":  # Changed back to actual condition
                                                print(f"{Fore.YELLOW}{EMOJI['INFO']} Account has reached maximum usage, deleting...{Style.RESET_ALL}")
                                                
                                                delete_js = """
                                                function deleteAccount() {
                                                    return new Promise((resolve, reject) => {
                                                        fetch('https://www.cursor.com/api/dashboard/delete-account', {
                                                            method: 'POST',
                                                            headers: {
                                                                'Content-Type': 'application/json'
                                                            },
                                                            credentials: 'include'
                                                        })
                                                        .then(response => {
                                                            if (response.status === 200) {
                                                                resolve('Account deleted successfully');
                                                            } else {
                                                                reject('Failed to delete account: ' + response.status);
                                                            }
                                                        })
                                                        .catch(error => {
                                                            reject('Error: ' + error);
                                                        });
                                                    });
                                                }
                                                return deleteAccount();
                                                """
                                                
                                                try:
                                                    result = self.browser.run_js(delete_js)
                                                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Delete account result: {result}{Style.RESET_ALL}")
                                                    
                                                    # Navigate back to auth page and repeat authentication
                                                    print(f"{Fore.CYAN}{EMOJI['INFO']} Starting re-authentication process...{Style.RESET_ALL}")
                                                    print(f"{Fore.CYAN}{EMOJI['INFO']} Redirecting to authenticator.cursor.sh...{Style.RESET_ALL}")
                                                    
                                                    # Explicitly navigate to the authentication page
                                                   #self.browser.get("https://authenticator.cursor.sh/sign-up")
                                                  #  time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                                                    
                                                    # Call handle_google_auth again to repeat the entire process
                                                    print(f"{Fore.CYAN}{EMOJI['INFO']} Starting new Google authentication...{Style.RESET_ALL}")
                                                    return self.handle_google_auth()
                                                    
                                                except Exception as e:
                                                    print(f"{Fore.RED}{EMOJI['ERROR']} Failed to delete account or re-authenticate: {str(e)}{Style.RESET_ALL}")
                                            else:
                                                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account is still valid (Usage: {usage_text}){Style.RESET_ALL}")
                                    except Exception as e:
                                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Could not find usage count: {str(e)}{Style.RESET_ALL}")
                                    
                                    # Remove the browser stay open prompt and input wait
                                    return True, {"email": actual_email, "token": token}
                        
                        # Also check URL as backup
                        current_url = self.browser.url
                        if "cursor.com/settings" in current_url:
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Already on settings page!{Style.RESET_ALL}")
                            time.sleep(1)
                            cookies = self.browser.cookies()
                            for cookie in cookies:
                                if cookie.get("name") == "WorkosCursorSessionToken":
                                    value = cookie.get("value", "")
                                    if "::" in value:
                                        token = value.split("::")[-1]
                                    elif "%3A%3A" in value:
                                        token = value.split("%3A%3A")[-1]
                                    if token:
                                        # Get email and check usage here too
                                        try:
                                            email_element = self.browser.ele("css:div[class='flex w-full flex-col gap-2'] div:nth-child(2) p:nth-child(2)")
                                            if email_element:
                                                actual_email = email_element.text
                                                print(f"{Fore.CYAN}{EMOJI['INFO']} Found email: {actual_email}{Style.RESET_ALL}")
                                        except Exception as e:
                                            print(f"{Fore.YELLOW}{EMOJI['INFO']} Could not find email: {str(e)}{Style.RESET_ALL}")
                                            actual_email = "user@cursor.sh"
                                        
                                        # Check usage count
                                        try:
                                            usage_element = self.browser.ele("css:div[class='flex flex-col gap-4 lg:flex-row'] div:nth-child(1) div:nth-child(1) span:nth-child(2)")
                                            if usage_element:
                                                usage_text = usage_element.text
                                                print(f"{Fore.CYAN}{EMOJI['INFO']} Usage count: {usage_text}{Style.RESET_ALL}")
                                                
                                                # Check if account is expired
                                                if usage_text.strip() == "150 / 150":  # Changed back to actual condition
                                                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Account has reached maximum usage, deleting...{Style.RESET_ALL}")
                                                    
                                                    delete_js = """
                                                    function deleteAccount() {
                                                        return new Promise((resolve, reject) => {
                                                            fetch('https://www.cursor.com/api/dashboard/delete-account', {
                                                                method: 'POST',
                                                                headers: {
                                                                    'Content-Type': 'application/json'
                                                                },
                                                                credentials: 'include'
                                                            })
                                                            .then(response => {
                                                                if (response.status === 200) {
                                                                    resolve('Account deleted successfully');
                                                                } else {
                                                                    reject('Failed to delete account: ' + response.status);
                                                                }
                                                            })
                                                            .catch(error => {
                                                                reject('Error: ' + error);
                                                            });
                                                        });
                                                    }
                                                    return deleteAccount();
                                                    """
                                                    
                                                    try:
                                                        result = self.browser.run_js(delete_js)
                                                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Delete account result: {result}{Style.RESET_ALL}")
                                                        
                                                        # Navigate back to auth page and repeat authentication
                                                        print(f"{Fore.CYAN}{EMOJI['INFO']} Starting re-authentication process...{Style.RESET_ALL}")
                                                        print(f"{Fore.CYAN}{EMOJI['INFO']} Redirecting to authenticator.cursor.sh...{Style.RESET_ALL}")
                                                        
                                                        # Explicitly navigate to the authentication page
                                                        self.browser.get("https://authenticator.cursor.sh/sign-up")
                                                        time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                                                        
                                                        # Call handle_google_auth again to repeat the entire process
                                                        print(f"{Fore.CYAN}{EMOJI['INFO']} Starting new Google authentication...{Style.RESET_ALL}")
                                                        return self.handle_google_auth()
                                                        
                                                    except Exception as e:
                                                        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to delete account or re-authenticate: {str(e)}{Style.RESET_ALL}")
                                            else:
                                                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account is still valid (Usage: {usage_text}){Style.RESET_ALL}")
                                        except Exception as e:
                                            print(f"{Fore.YELLOW}{EMOJI['INFO']} Could not find usage count: {str(e)}{Style.RESET_ALL}")
                                        
                                        # Remove the browser stay open prompt and input wait
                                        return True, {"email": actual_email, "token": token}
                        elif current_url != last_url:
                            print(f"{Fore.CYAN}{EMOJI['INFO']} Page changed, checking auth...{Style.RESET_ALL}")
                            last_url = current_url
                            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                    except Exception as e:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Status check error: {str(e)}{Style.RESET_ALL}")
                        time.sleep(1)
                        continue
                    time.sleep(1)
                    
                print(f"{Fore.RED}{EMOJI['ERROR']} Authentication timeout{Style.RESET_ALL}")
                return False, None
                
            print(f"{Fore.RED}{EMOJI['ERROR']} Authentication button not found{Style.RESET_ALL}")
            return False, None
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Authentication failed: {str(e)}{Style.RESET_ALL}")
            return False, None
        finally:
            if self.browser:
                self.browser.quit()

    def _extract_auth_info(self):
        """Extract authentication information after successful OAuth"""
        try:
            # Get cookies with retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    cookies = self.browser.cookies()
                    if cookies:
                        break
                    time.sleep(1)
                except:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(1)
            
            # Debug cookie information
            print(f"{Fore.CYAN}{EMOJI['INFO']} Found {len(cookies)} cookies{Style.RESET_ALL}")
            
            email = None
            token = None
            
            for cookie in cookies:
                name = cookie.get("name", "")
                if name == "WorkosCursorSessionToken":
                    try:
                        value = cookie.get("value", "")
                        if "::" in value:
                            token = value.split("::")[-1]
                        elif "%3A%3A" in value:
                            token = value.split("%3A%3A")[-1]
                    except Exception as e:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Token extraction error: {str(e)}{Style.RESET_ALL}")
                elif name == "cursor_email":
                    email = cookie.get("value")
                    
            if email and token:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Authentication successful - Email: {email}{Style.RESET_ALL}")
                return True, {"email": email, "token": token}
            else:
                missing = []
                if not email:
                    missing.append("email")
                if not token:
                    missing.append("token")
                print(f"{Fore.RED}{EMOJI['ERROR']} Missing authentication data: {', '.join(missing)}{Style.RESET_ALL}")
                return False, None
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to extract auth info: {str(e)}{Style.RESET_ALL}")
            return False, None

def main(auth_type, translator=None):
    """Main function to handle OAuth authentication
    
    Args:
        auth_type (str): Type of authentication ('google' or 'github')
        translator: Translator instance for internationalization
    """
    handler = OAuthHandler(translator)
    
    if auth_type.lower() == 'google':
        success, auth_info = handler.handle_google_auth()
    elif auth_type.lower() == 'github':
        success, auth_info = handler.handle_github_auth()
    else:
        print(f"{Fore.RED}{EMOJI['ERROR']} Invalid authentication type{Style.RESET_ALL}")
        return False
        
    if success and auth_info:
        # Update Cursor authentication
        auth_manager = CursorAuth(translator)
        if auth_manager.update_auth(
            email=auth_info["email"],
            access_token=auth_info["token"],
            refresh_token=auth_info["token"]
        ):
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Cursor authentication updated successfully{Style.RESET_ALL}")
            # Close the browser after successful authentication
            if handler.browser:
                handler.browser.quit()
                print(f"{Fore.CYAN}{EMOJI['INFO']} Browser closed{Style.RESET_ALL}")
            return True
            
    return False 
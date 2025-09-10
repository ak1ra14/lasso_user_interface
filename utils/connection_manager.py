
# import threading
# import time
# import socket
# import subprocess
# import re
# from kivy.clock import Clock
# from kivy.logger import Logger
# from kivy.app import App

# class ConnectionManager:
#     """
#     Complete connection manager for monitoring WiFi and network status
#     Runs in background thread to avoid UI blocking
#     """
    
#     def __init__(self, app_instance):
#         self.app = app_instance
#         self.is_running = False
#         self.connection_thread = None
        
#         # Current status tracking
#         self.last_connection_status = None
#         self.last_ssid = None
#         self.last_ip_address = None
        
#         # Configuration
#         self.check_interval = 30  # seconds between checks
#         self.quick_check_timeout = 2  # seconds for quick check
#         self.full_check_timeout = 5   # seconds for thorough check
        
#         # Multiple test hosts for redundancy
#         self.test_hosts = [
#             ("1.1.1.1", 53),        # Cloudflare DNS (usually fastest)
#             ("8.8.8.8", 53),        # Google DNS
#             ("208.67.222.222", 53), # OpenDNS
#             ("9.9.9.9", 53),        # Quad9 DNS
#         ]
        
#         Logger.info("ConnectionManager: Initialized")
    
#     def start_monitoring(self):
#         """Start the background connection monitoring"""
#         if self.is_running:
#             Logger.warning("ConnectionManager: Already running")
#             return
            
#         self.is_running = True
#         self.connection_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
#         self.connection_thread.start()
#         Logger.info("ConnectionManager: Started background monitoring")
        
#         # Do an immediate check
#         self.force_check()
    
#     def stop_monitoring(self):
#         """Stop the background connection monitoring"""
#         if not self.is_running:
#             return
            
#         Logger.info("ConnectionManager: Stopping background monitoring")
#         self.is_running = False
        
#         if self.connection_thread and self.connection_thread.is_alive():
#             self.connection_thread.join(timeout=3)
            
#         Logger.info("ConnectionManager: Background monitoring stopped")
    
#     def _monitoring_loop(self):
#         """Main monitoring loop running in background thread"""
#         Logger.info("ConnectionManager: Monitoring loop started")
        
#         while self.is_running:
#             try:
#                 # Perform connection check
#                 connection_info = self._full_connection_check()
                
#                 # Check if anything changed
#                 if self._has_status_changed(connection_info):
#                     Logger.info(f"ConnectionManager: Status changed - {connection_info}")
#                     # Schedule UI update on main thread
#                     Clock.schedule_once(
#                         lambda dt: self._update_ui(connection_info), 0
#                     )
#                     self._update_status_cache(connection_info)
                
#                 # Wait for next check (with early exit capability)
#                 self._wait_with_early_exit(self.check_interval)
                
#             except Exception as e:
#                 Logger.error(f"ConnectionManager: Error in monitoring loop: {e}")
#                 self._wait_with_early_exit(5)  # Wait 5 seconds before retry
    
#     def _full_connection_check(self):
#         """
#         Comprehensive connection check
#         Returns dict with connection info
#         """
#         # Quick connectivity test first
#         is_connected = self._test_internet_connectivity()
        
#         connection_info = {
#             'is_connected': is_connected,
#             'ssid': None,
#             'ip_address': None,
#             'interface': None
#         }
        
#         if is_connected:
#             # Get WiFi information
#             wifi_info = self._get_wifi_info()
#             connection_info.update(wifi_info)
            
#             # Get IP address
#             ip_address = self._get_ip_address()
#             connection_info['ip_address'] = ip_address
        
#         return connection_info
    
#     def _test_internet_connectivity(self):
#         """Test internet connectivity using multiple methods"""
        
#         # Method 1: Quick check with short timeout
#         if self._quick_connectivity_test():
#             return True
        
#         # Method 2: Thorough check with multiple hosts
#         return self._thorough_connectivity_test()
    
#     def _quick_connectivity_test(self):
#         """Quick connectivity test (1-2 seconds)"""
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(self.quick_check_timeout)
#             result = sock.connect_ex(("1.1.1.1", 53))  # Cloudflare DNS
#             sock.close()
#             return result == 0
#         except Exception:
#             return False
    
#     def _thorough_connectivity_test(self):
#         """Thorough connectivity test with multiple hosts"""
#         for host, port in self.test_hosts:
#             if self._test_single_host(host, port):
#                 return True
#         return False
    
#     def _test_single_host(self, host, port):
#         """Test connectivity to a single host"""
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(self.full_check_timeout)
#             result = sock.connect_ex((host, port))
#             sock.close()
#             return result == 0
#         except Exception:
#             return False
    
#     def _get_wifi_info(self):
#         """Get current WiFi SSID and interface information"""
#         try:
#             # Try different methods based on platform
#             import sys
            
#             if sys.platform.startswith('linux'):
#                 return self._get_wifi_info_linux()
#             elif sys.platform == 'darwin':  # macOS
#                 return self._get_wifi_info_macos()
#             elif sys.platform.startswith('win'):
#                 return self._get_wifi_info_windows()
#             else:
#                 return {'ssid': 'Unknown', 'interface': 'Unknown'}
                
#         except Exception as e:
#             Logger.error(f"ConnectionManager: Error getting WiFi info: {e}")
#             return {'ssid': None, 'interface': None}
    
#     def _get_wifi_info_linux(self):
#         """Get WiFi info on Linux systems"""
#         try:
#             # Try iwgetid first (most reliable)
#             result = subprocess.run(['iwgetid', '-r'], 
#                                   capture_output=True, text=True, timeout=5)
#             if result.returncode == 0:
#                 ssid = result.stdout.strip()
#                 if ssid:
#                     return {'ssid': ssid, 'interface': 'wifi'}
            
#             # Fallback: try nmcli
#             result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], 
#                                   capture_output=True, text=True, timeout=5)
#             if result.returncode == 0:
#                 for line in result.stdout.split('\n'):
#                     if line.startswith('yes:'):
#                         ssid = line.split(':', 1)[1].strip()
#                         if ssid:
#                             return {'ssid': ssid, 'interface': 'wifi'}
            
#             return {'ssid': None, 'interface': None}
            
#         except Exception as e:
#             Logger.error(f"ConnectionManager: Linux WiFi info error: {e}")
#             return {'ssid': None, 'interface': None}
    
#     def _get_wifi_info_macos(self):
#         """Get WiFi info on macOS"""
#         try:
#             result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], 
#                                   capture_output=True, text=True, timeout=5)
#             if result.returncode == 0:
#                 for line in result.stdout.split('\n'):
#                     if ' SSID:' in line:
#                         ssid = line.split('SSID:', 1)[1].strip()
#                         if ssid:
#                             return {'ssid': ssid, 'interface': 'wifi'}
            
#             return {'ssid': None, 'interface': None}
            
#         except Exception as e:
#             Logger.error(f"ConnectionManager: macOS WiFi info error: {e}")
#             return {'ssid': None, 'interface': None}
    
#     def _get_wifi_info_windows(self):
#         """Get WiFi info on Windows"""
#         try:
#             result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
#                                   capture_output=True, text=True, timeout=5)
#             # This is a simplified version - Windows WiFi detection is complex
#             # You might want to use a more robust method
#             return {'ssid': 'Windows WiFi', 'interface': 'wifi'}
            
#         except Exception as e:
#             Logger.error(f"ConnectionManager: Windows WiFi info error: {e}")
#             return {'ssid': None, 'interface': None}
    
#     def _get_ip_address(self):
#         """Get current IP address"""
#         try:
#             # Method 1: Connect to external host to get local IP
#             sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             sock.settimeout(3)
#             sock.connect(("8.8.8.8", 80))
#             ip_address = sock.getsockname()[0]
#             sock.close()
#             return ip_address
            
#         except Exception:
#             try:
#                 # Method 2: Get hostname IP
#                 hostname = socket.gethostname()
#                 return socket.gethostbyname(hostname)
#             except Exception:
#                 return None
    
#     def _has_status_changed(self, connection_info):
#         """Check if connection status has changed"""
#         return (
#             connection_info['is_connected'] != self.last_connection_status or
#             connection_info['ssid'] != self.last_ssid or
#             connection_info['ip_address'] != self.last_ip_address
#         )
    
#     def _update_status_cache(self, connection_info):
#         """Update cached status"""
#         self.last_connection_status = connection_info['is_connected']
#         self.last_ssid = connection_info['ssid']
#         self.last_ip_address = connection_info['ip_address']
    
#     def _update_ui(self, connection_info):
#         """Update UI on main thread - must be called from main thread"""
#         try:
#             # Import here to avoid circular imports
#             from utils.config_loader import save_config, update_text_language
            
#             # Update app configuration
#             if connection_info['is_connected'] and connection_info['ssid']:
#                 self.app.config['wifi_ssid'] = connection_info['ssid']

#                 if connection_info['ip_address']:
#                     self.app.ip_address = connection_info['ip_address']
#                     ip_text = f"{update_text_language('ip_address')}: {connection_info['ip_address']}"
#                 else:
#                     ip_text = f"{update_text_language('ip_address')}: {update_text_language('connected')}"
#             else:
#                 self.app.config['wifi_ssid'] = 'Not Connected'
#                 ip_text = f"{update_text_language('ip_address')}: {update_text_language('not_connected')}"
            
#             # Save configuration
#             save_config('config/settings.json', 'v3_json', data=self.app.config)
            
#             # Update monitor screen if available
#             try:
#                 Logger.debug("updating icons")
#                 menu_screen = self.app.sm.get_screen('menu2')
#                 menu_screen.content_buttons['wi-fi'].status.text = connection_info['ssid'] if connection_info['ssid'] else update_text_language('not_connected')
#                 menu_screen.content_buttons['wi-fi'].image.source = "images/wifi.png" if connection_info['ssid'] else "images.wifi_not_connected"
#                 Logger.debug("wifi updated")
#                 monitor_screen = self.app.sm.get_screen('monitor')
#                 if hasattr(monitor_screen, 'ip_label'):
#                     monitor_screen.ip_label.text = ip_text
                
#             except Exception as e:
#                 Logger.debug(f"ConnectionManager: Monitor screen not available: {e}")
            
#             Logger.info(f"ConnectionManager: UI updated - Connected: {connection_info['is_connected']}, SSID: {connection_info['ssid']}")
            
#         except Exception as e:
#             Logger.error(f"ConnectionManager: Error updating UI: {e}")
    
#     def _wait_with_early_exit(self, seconds):
#         """Wait for specified seconds with ability to exit early"""
#         for _ in range(int(seconds)):
#             if not self.is_running:
#                 break
#             time.sleep(1)
    
#     def force_check(self):
#         """Force an immediate connection check in background"""
#         def immediate_check():
#             try:
#                 connection_info = self._full_connection_check()
#                 Clock.schedule_once(lambda dt: self._update_ui(connection_info), 0)
#                 self._update_status_cache(connection_info)
#                 Logger.info("ConnectionManager: Force check completed")
#             except Exception as e:
#                 Logger.error(f"ConnectionManager: Force check error: {e}")
        
#         if self.is_running:
#             threading.Thread(target=immediate_check, daemon=True).start()
#         else:
#             Logger.warning("ConnectionManager: Cannot force check - not running")
    
#     def get_current_status(self):
#         """Get current cached status (non-blocking)"""
#         return {
#             'is_connected': self.last_connection_status,
#             'ssid': self.last_ssid,
#             'ip_address': self.last_ip_address
#         }
    
#     def set_check_interval(self, seconds):
#         """Change the check interval"""
#         self.check_interval = max(10, seconds)  # Minimum 10 seconds
#         Logger.info(f"ConnectionManager: Check interval set to {self.check_interval} seconds")


import os
import socket
import threading
import time
import subprocess
import configparser
import re
from kivy.clock import Clock
from kivy.logger import Logger
from utils.config_loader import load_config, save_config, update_text_language
from screens.monitor import get_ip_address
from screens.wifi import get_connected_wifi


class ConnectionManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.monitoring = False
        self.monitor_thread = None
        self.check_interval = 30  # Check every 30 seconds
        self.last_connection_status = None
        self.last_ssid = None
        self.last_ip = None
        self.wifi_credentials_cache = {}  # Cache for retrieved passwords
        
    def start_monitoring(self):
        """Start the connection monitoring thread"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            Logger.info("ConnectionManager: Monitoring started")
    
    def stop_monitoring(self):
        """Stop the connection monitoring thread"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        Logger.info("ConnectionManager: Monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop running in separate thread"""
        while self.monitoring:
            try:
                # Check connection status
                is_connected = self._check_internet_connection()
                current_ssid = get_connected_wifi()
                current_ip = get_ip_address() if is_connected else None
                
                # Check if status changed
                status_changed = (
                    is_connected != self.last_connection_status or
                    current_ssid != self.last_ssid or
                    current_ip != self.last_ip
                )
                
                if status_changed:
                    # Schedule UI update on main thread
                    Clock.schedule_once(
                        lambda dt: self._update_connection_status(
                            is_connected, current_ssid, current_ip
                        )
                    )
                    
                    # Update last known values
                    self.last_connection_status = is_connected
                    self.last_ssid = current_ssid
                    self.last_ip = current_ip
                
            except Exception as e:
                Logger.error(f"ConnectionManager: Error in monitoring loop: {e}")
            
            # Wait before next check
            time.sleep(self.check_interval)
    
    def _check_internet_connection(self, host="8.8.8.8", port=53, timeout=3):
        """
        Check if there's an active internet connection
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False
    
    def _update_connection_status(self, is_connected, ssid, ip_address):
        """
        Update connection status in config and UI (runs on main thread)
        """
        try:
            # Load current config
            config = load_config('config/settings.json', 'v3_json')
            
            if is_connected and ssid:
                Logger.info(f"ConnectionManager: Connected to Wi-Fi: {ssid}")
                config['wifi_ssid'] = ssid
                
                # Try to get and store WiFi credentials
                password = self.get_wifi_password(ssid)
                if password:
                    config['wifi_password'] = password
                    Logger.info(f"ConnectionManager: Retrieved password for {ssid}")
                
                # Update IP address
                if ip_address:
                    self.app.ip_address = ip_address
                    
                    # Update monitor screen
                    monitor_screen = self.app.sm.get_screen('monitor')
                    if hasattr(monitor_screen, 'ip_label'):
                        monitor_screen.ip_label.text = f"{update_text_language('ip_address')}: {ip_address}"
                
            else:
                Logger.info("ConnectionManager: Not connected to Wi-Fi")
                config['wifi_ssid'] = 'Not connected'
                
                # Update monitor screen
                monitor_screen = self.app.sm.get_screen('monitor')
                if hasattr(monitor_screen, 'ip_label'):
                    monitor_screen.ip_label.text = f"{update_text_language('ip_address')}: {update_text_language('not_connected')}"
            
            # Update monitor screen if available
            
                Logger.debug("updating icons")

            menu_screen = self.app.sm.get_screen('menu2')
            menu_screen.content_buttons['wi-fi'].status.text = config['wifi_ssid'] if config['wifi_ssid'] != 'Not connected' else update_text_language('not_connected')
            menu_screen.content_buttons['wi-fi'].image.source = "images/wifi.png" if config['wifi_ssid'] != 'Not connected' else "images.wifi_not_connected"

            # Save updated config
            save_config('config/settings.json', 'v3_json', data=config)
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Error updating connection status: {e}")
    
    def get_wifi_password(self, ssid):
        """
        Retrieve WiFi password for a given SSID
        Returns the password if found, None otherwise
        """
        # Check cache first
        if ssid in self.wifi_credentials_cache:
            return self.wifi_credentials_cache[ssid]
        
        password = None
        
        try:
            # Try different methods based on the system
            password = (
                self._get_password_networkmanager(ssid) or
                self._get_password_wpa_supplicant(ssid) or
                self._get_password_windows(ssid) or
                self._get_password_macos(ssid)
            )
            
            # Cache the result (even if None)
            self.wifi_credentials_cache[ssid] = password
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Error retrieving password for {ssid}: {e}")
        
        return password
    
    def _get_password_networkmanager(self, ssid):
        """
        Get password from NetworkManager (Linux)
        """
        try:
            nm_path = "/etc/NetworkManager/system-connections/"
            
            if not os.path.exists(nm_path):
                return None
                
            for filename in os.listdir(nm_path):
                filepath = os.path.join(nm_path, filename)
                
                try:
                    config = configparser.ConfigParser()
                    config.read(filepath)
                    
                    # Check if this is the right SSID
                    if 'wifi' in config:
                        stored_ssid = config['wifi'].get('ssid', '').strip('"')
                        if stored_ssid == ssid:
                            # Get password
                            if 'wifi-security' in config:
                                psk = config['wifi-security'].get('psk', '').strip('"')
                                if psk:
                                    return psk
                    
                except Exception:
                    # Try reading as plain text file
                    with open(filepath, 'r') as f:
                        content = f.read()
                        
                    if f'ssid={ssid}' in content or f'ssid="{ssid}"' in content:
                        for line in content.split('\n'):
                            if line.startswith('psk='):
                                return line.split('=', 1)[1].strip('"')
                                
                except (PermissionError, FileNotFoundError):
                    continue
                    
        except Exception as e:
            Logger.debug(f"ConnectionManager: NetworkManager method failed: {e}")
            
        return None
    
    def _get_password_wpa_supplicant(self, ssid):
        """
        Get password from wpa_supplicant configuration (Linux)
        """
        try:
            wpa_config_paths = [
                '/etc/wpa_supplicant/wpa_supplicant.conf',
                '/etc/wpa_supplicant.conf'
            ]
            
            for config_path in wpa_config_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        content = f.read()
                    
                    # Parse networks
                    networks = re.findall(r'network=\{[^}]+\}', content, re.DOTALL)
                    
                    for network in networks:
                        if f'ssid="{ssid}"' in network or f"ssid='{ssid}'" in network:
                            psk_match = re.search(r'psk="([^"]+)"', network)
                            if not psk_match:
                                psk_match = re.search(r"psk='([^']+)'", network)
                            if psk_match:
                                return psk_match.group(1)
                                
        except Exception as e:
            Logger.debug(f"ConnectionManager: wpa_supplicant method failed: {e}")
            
        return None
    
    def _get_password_windows(self, ssid):
        """
        Get password from Windows using netsh (Windows)
        """
        try:
            import platform
            if not platform.system() == 'Windows':
                return None
                
            result = subprocess.run([
                'netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                password_match = re.search(r'Key Content\s*:\s*(.+)', result.stdout)
                if password_match:
                    return password_match.group(1).strip()
                    
        except Exception as e:
            Logger.debug(f"ConnectionManager: Windows method failed: {e}")
            
        return None
    
    def _get_password_macos(self, ssid):
        """
        Get password from macOS Keychain (macOS)
        """
        try:
            import platform
            if not platform.system() == 'Darwin':
                return None
                
            result = subprocess.run([
                'security', 'find-generic-password',
                '-D', 'AirPort network password',
                '-a', ssid,
                '-w'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return result.stdout.strip()
                
        except Exception as e:
            Logger.debug(f"ConnectionManager: macOS method failed: {e}")
            
        return None
    
    def get_current_wifi_credentials(self):
        """
        Get credentials for currently connected WiFi network
        Returns tuple (ssid, password) or (None, None) if not available
        """
        try:
            current_ssid = get_connected_wifi()
            if not current_ssid:
                return None, None
                
            password = self.get_wifi_password(current_ssid)
            return current_ssid, password
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Error getting current credentials: {e}")
            return None, None
    
    def get_all_saved_wifi_credentials(self):
        """
        Get all saved WiFi credentials on the system
        Returns dictionary {ssid: password}
        """
        credentials = {}
        
        try:
            # Try NetworkManager
            nm_credentials = self._get_all_networkmanager_credentials()
            credentials.update(nm_credentials)
            
            # Try wpa_supplicant
            wpa_credentials = self._get_all_wpa_supplicant_credentials()
            credentials.update(wpa_credentials)
            
            # Try Windows
            win_credentials = self._get_all_windows_credentials()
            credentials.update(win_credentials)
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Error getting all credentials: {e}")
        
        return credentials
    
    def _get_all_networkmanager_credentials(self):
        """Get all NetworkManager saved networks"""
        credentials = {}
        try:
            nm_path = "/etc/NetworkManager/system-connections/"
            if os.path.exists(nm_path):
                for filename in os.listdir(nm_path):
                    filepath = os.path.join(nm_path, filename)
                    try:
                        config = configparser.ConfigParser()
                        config.read(filepath)
                        
                        if 'wifi' in config and 'wifi-security' in config:
                            ssid = config['wifi'].get('ssid', '').strip('"')
                            psk = config['wifi-security'].get('psk', '').strip('"')
                            if ssid and psk:
                                credentials[ssid] = psk
                    except Exception:
                        continue
        except Exception as e:
            Logger.debug(f"ConnectionManager: Error getting NetworkManager credentials: {e}")
        
        return credentials
    
    def _get_all_wpa_supplicant_credentials(self):
        """Get all wpa_supplicant saved networks"""
        credentials = {}
        try:
            wpa_config_paths = [
                '/etc/wpa_supplicant/wpa_supplicant.conf',
                '/etc/wpa_supplicant.conf'
            ]
            
            for config_path in wpa_config_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        content = f.read()
                    
                    networks = re.findall(r'network=\{[^}]+\}', content, re.DOTALL)
                    
                    for network in networks:
                        ssid_match = re.search(r'ssid="([^"]+)"', network)
                        if not ssid_match:
                            ssid_match = re.search(r"ssid='([^']+)'", network)
                            
                        psk_match = re.search(r'psk="([^"]+)"', network)
                        if not psk_match:
                            psk_match = re.search(r"psk='([^']+)'", network)
                            
                        if ssid_match and psk_match:
                            credentials[ssid_match.group(1)] = psk_match.group(1)
                            
        except Exception as e:
            Logger.debug(f"ConnectionManager: Error getting wpa_supplicant credentials: {e}")
        
        return credentials
    
    def _get_all_windows_credentials(self):
        """Get all Windows saved networks"""
        credentials = {}
        try:
            import platform
            if not platform.system() == 'Windows':
                return credentials
                
            # Get list of profiles
            profiles_result = subprocess.run([
                'netsh', 'wlan', 'show', 'profiles'
            ], capture_output=True, text=True, timeout=15)
            
            profiles = re.findall(r'Profile\s*:\s*(.+)', profiles_result.stdout)
            
            for profile in profiles:
                profile = profile.strip()
                password = self._get_password_windows(profile)
                if password:
                    credentials[profile] = password
                    
        except Exception as e:
            Logger.debug(f"ConnectionManager: Error getting Windows credentials: {e}")
        
        return credentials
    
    def clear_credentials_cache(self):
        """Clear the credentials cache"""
        self.wifi_credentials_cache.clear()
        Logger.info("ConnectionManager: Credentials cache cleared")
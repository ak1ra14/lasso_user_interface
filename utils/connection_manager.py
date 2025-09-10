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
            menu_screen.content_buttons['wi-fi'].image.source = "images/wifi.png" if config['wifi_ssid'] != 'Not connected' else "images/wifi_not_connected.png"

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
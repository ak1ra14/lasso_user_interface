
import threading
import time
import socket
import subprocess
import re
from kivy.clock import Clock
from kivy.logger import Logger

class ConnectionManager:
    """
    Complete connection manager for monitoring WiFi and network status
    Runs in background thread to avoid UI blocking
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.is_running = False
        self.connection_thread = None
        
        # Current status tracking
        self.last_connection_status = None
        self.last_ssid = None
        self.last_ip_address = None
        
        # Configuration
        self.check_interval = 30  # seconds between checks
        self.quick_check_timeout = 2  # seconds for quick check
        self.full_check_timeout = 5   # seconds for thorough check
        
        # Multiple test hosts for redundancy
        self.test_hosts = [
            ("1.1.1.1", 53),        # Cloudflare DNS (usually fastest)
            ("8.8.8.8", 53),        # Google DNS
            ("208.67.222.222", 53), # OpenDNS
            ("9.9.9.9", 53),        # Quad9 DNS
        ]
        
        Logger.info("ConnectionManager: Initialized")
    
    def start_monitoring(self):
        """Start the background connection monitoring"""
        if self.is_running:
            Logger.warning("ConnectionManager: Already running")
            return
            
        self.is_running = True
        self.connection_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.connection_thread.start()
        Logger.info("ConnectionManager: Started background monitoring")
        
        # Do an immediate check
        self.force_check()
    
    def stop_monitoring(self):
        """Stop the background connection monitoring"""
        if not self.is_running:
            return
            
        Logger.info("ConnectionManager: Stopping background monitoring")
        self.is_running = False
        
        if self.connection_thread and self.connection_thread.is_alive():
            self.connection_thread.join(timeout=3)
            
        Logger.info("ConnectionManager: Background monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in background thread"""
        Logger.info("ConnectionManager: Monitoring loop started")
        
        while self.is_running:
            try:
                # Perform connection check
                connection_info = self._full_connection_check()
                
                # Check if anything changed
                if self._has_status_changed(connection_info):
                    Logger.info(f"ConnectionManager: Status changed - {connection_info}")
                    # Schedule UI update on main thread
                    Clock.schedule_once(
                        lambda dt: self._update_ui(connection_info), 0
                    )
                    self._update_status_cache(connection_info)
                
                # Wait for next check (with early exit capability)
                self._wait_with_early_exit(self.check_interval)
                
            except Exception as e:
                Logger.error(f"ConnectionManager: Error in monitoring loop: {e}")
                self._wait_with_early_exit(5)  # Wait 5 seconds before retry
    
    def _full_connection_check(self):
        """
        Comprehensive connection check
        Returns dict with connection info
        """
        # Quick connectivity test first
        is_connected = self._test_internet_connectivity()
        
        connection_info = {
            'is_connected': is_connected,
            'ssid': None,
            'ip_address': None,
            'interface': None
        }
        
        if is_connected:
            # Get WiFi information
            wifi_info = self._get_wifi_info()
            connection_info.update(wifi_info)
            
            # Get IP address
            ip_address = self._get_ip_address()
            connection_info['ip_address'] = ip_address
        
        return connection_info
    
    def _test_internet_connectivity(self):
        """Test internet connectivity using multiple methods"""
        
        # Method 1: Quick check with short timeout
        if self._quick_connectivity_test():
            return True
        
        # Method 2: Thorough check with multiple hosts
        return self._thorough_connectivity_test()
    
    def _quick_connectivity_test(self):
        """Quick connectivity test (1-2 seconds)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.quick_check_timeout)
            result = sock.connect_ex(("1.1.1.1", 53))  # Cloudflare DNS
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _thorough_connectivity_test(self):
        """Thorough connectivity test with multiple hosts"""
        for host, port in self.test_hosts:
            if self._test_single_host(host, port):
                return True
        return False
    
    def _test_single_host(self, host, port):
        """Test connectivity to a single host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.full_check_timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _get_wifi_info(self):
        """Get current WiFi SSID and interface information"""
        try:
            # Try different methods based on platform
            import sys
            
            if sys.platform.startswith('linux'):
                return self._get_wifi_info_linux()
            elif sys.platform == 'darwin':  # macOS
                return self._get_wifi_info_macos()
            elif sys.platform.startswith('win'):
                return self._get_wifi_info_windows()
            else:
                return {'ssid': 'Unknown', 'interface': 'Unknown'}
                
        except Exception as e:
            Logger.error(f"ConnectionManager: Error getting WiFi info: {e}")
            return {'ssid': None, 'interface': None}
    
    def _get_wifi_info_linux(self):
        """Get WiFi info on Linux systems"""
        try:
            # Try iwgetid first (most reliable)
            result = subprocess.run(['iwgetid', '-r'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                ssid = result.stdout.strip()
                if ssid:
                    return {'ssid': ssid, 'interface': 'wifi'}
            
            # Fallback: try nmcli
            result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('yes:'):
                        ssid = line.split(':', 1)[1].strip()
                        if ssid:
                            return {'ssid': ssid, 'interface': 'wifi'}
            
            return {'ssid': None, 'interface': None}
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Linux WiFi info error: {e}")
            return {'ssid': None, 'interface': None}
    
    def _get_wifi_info_macos(self):
        """Get WiFi info on macOS"""
        try:
            result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ' SSID:' in line:
                        ssid = line.split('SSID:', 1)[1].strip()
                        if ssid:
                            return {'ssid': ssid, 'interface': 'wifi'}
            
            return {'ssid': None, 'interface': None}
            
        except Exception as e:
            Logger.error(f"ConnectionManager: macOS WiFi info error: {e}")
            return {'ssid': None, 'interface': None}
    
    def _get_wifi_info_windows(self):
        """Get WiFi info on Windows"""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, timeout=5)
            # This is a simplified version - Windows WiFi detection is complex
            # You might want to use a more robust method
            return {'ssid': 'Windows WiFi', 'interface': 'wifi'}
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Windows WiFi info error: {e}")
            return {'ssid': None, 'interface': None}
    
    def _get_ip_address(self):
        """Get current IP address"""
        try:
            # Method 1: Connect to external host to get local IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            sock.connect(("8.8.8.8", 80))
            ip_address = sock.getsockname()[0]
            sock.close()
            return ip_address
            
        except Exception:
            try:
                # Method 2: Get hostname IP
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except Exception:
                return None
    
    def _has_status_changed(self, connection_info):
        """Check if connection status has changed"""
        return (
            connection_info['is_connected'] != self.last_connection_status or
            connection_info['ssid'] != self.last_ssid or
            connection_info['ip_address'] != self.last_ip_address
        )
    
    def _update_status_cache(self, connection_info):
        """Update cached status"""
        self.last_connection_status = connection_info['is_connected']
        self.last_ssid = connection_info['ssid']
        self.last_ip_address = connection_info['ip_address']
    
    def _update_ui(self, connection_info):
        """Update UI on main thread - must be called from main thread"""
        try:
            # Import here to avoid circular imports
            from utils.config_loader import save_config, update_text_language
            
            # Update app configuration
            if connection_info['is_connected'] and connection_info['ssid']:
                self.app.config['wifi_ssid'] = connection_info['ssid']
                if connection_info['ip_address']:
                    self.app.ip_address = connection_info['ip_address']
                    ip_text = f"{update_text_language('ip_address')}: {connection_info['ip_address']}"
                else:
                    ip_text = f"{update_text_language('ip_address')}: {update_text_language('connected')}"
            else:
                self.app.config['wifi_ssid'] = 'Not connected'
                ip_text = f"{update_text_language('ip_address')}: {update_text_language('not_connected')}"
            
            # Save configuration
            save_config('config/settings.json', 'v3_json', data=self.app.config)
            
            # Update monitor screen if available
            try:
                monitor_screen = self.app.sm.get_screen('monitor')
                if hasattr(monitor_screen, 'ip_label'):
                    monitor_screen.ip_label.text = ip_text
            except Exception as e:
                Logger.debug(f"ConnectionManager: Monitor screen not available: {e}")
            
            Logger.info(f"ConnectionManager: UI updated - Connected: {connection_info['is_connected']}, SSID: {connection_info['ssid']}")
            
        except Exception as e:
            Logger.error(f"ConnectionManager: Error updating UI: {e}")
    
    def _wait_with_early_exit(self, seconds):
        """Wait for specified seconds with ability to exit early"""
        for _ in range(int(seconds)):
            if not self.is_running:
                break
            time.sleep(1)
    
    def force_check(self):
        """Force an immediate connection check in background"""
        def immediate_check():
            try:
                connection_info = self._full_connection_check()
                Clock.schedule_once(lambda dt: self._update_ui(connection_info), 0)
                self._update_status_cache(connection_info)
                Logger.info("ConnectionManager: Force check completed")
            except Exception as e:
                Logger.error(f"ConnectionManager: Force check error: {e}")
        
        if self.is_running:
            threading.Thread(target=immediate_check, daemon=True).start()
        else:
            Logger.warning("ConnectionManager: Cannot force check - not running")
    
    def get_current_status(self):
        """Get current cached status (non-blocking)"""
        return {
            'is_connected': self.last_connection_status,
            'ssid': self.last_ssid,
            'ip_address': self.last_ip_address
        }
    
    def set_check_interval(self, seconds):
        """Change the check interval"""
        self.check_interval = max(10, seconds)  # Minimum 10 seconds
        Logger.info(f"ConnectionManager: Check interval set to {self.check_interval} seconds")

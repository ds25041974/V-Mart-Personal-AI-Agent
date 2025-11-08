"""
Screen Reader Module
Detects and captures data from active windows on the system
Supports: Excel, Google Sheets, Tableau, PowerPoint, Email clients
"""

import os
import platform
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional


class ScreenReader:
    """Detects and identifies active windows and applications"""

    def __init__(self):
        self.system = platform.system()
        self.active_windows = []

    def get_active_window_info(self) -> Dict[str, Any]:
        """Get information about the currently active window"""
        if self.system == "Darwin":  # macOS
            return self._get_active_window_macos()
        elif self.system == "Windows":
            return self._get_active_window_windows()
        elif self.system == "Linux":
            return self._get_active_window_linux()
        return {}

    def _get_active_window_macos(self) -> Dict[str, Any]:
        """Get active window information on macOS using AppleScript"""
        try:
            # Get frontmost application
            script = """
            tell application "System Events"
                set frontApp to first application process whose frontmost is true
                set appName to name of frontApp
                
                try
                    set windowTitle to name of front window of frontApp
                on error
                    set windowTitle to ""
                end try
                
                return appName & "|" & windowTitle
            end tell
            """

            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                parts = result.stdout.strip().split("|")
                app_name = parts[0] if len(parts) > 0 else ""
                window_title = parts[1] if len(parts) > 1 else ""

                return {
                    "application": app_name,
                    "window_title": window_title,
                    "app_type": self._identify_app_type(app_name, window_title),
                    "timestamp": datetime.now().isoformat(),
                }
        except Exception as e:
            print(f"Error getting active window on macOS: {e}")

        return {}

    def _get_active_window_windows(self) -> Dict[str, Any]:
        """Get active window information on Windows using PowerShell"""
        try:
            script = """
            Add-Type @"
                using System;
                using System.Runtime.InteropServices;
                public class Window {
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    [DllImport("user32.dll")]
                    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
                }
"@
            $handle = [Window]::GetForegroundWindow()
            $title = New-Object System.Text.StringBuilder(256)
            [Window]::GetWindowText($handle, $title, 256)
            $title.ToString()
            """

            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                window_title = result.stdout.strip()
                return {
                    "application": "Unknown",
                    "window_title": window_title,
                    "app_type": self._identify_app_type("", window_title),
                    "timestamp": datetime.now().isoformat(),
                }
        except Exception as e:
            print(f"Error getting active window on Windows: {e}")

        return {}

    def _get_active_window_linux(self) -> Dict[str, Any]:
        """Get active window information on Linux using xdotool"""
        try:
            # Get active window ID
            result = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                window_id = result.stdout.strip()

                # Get window name
                name_result = subprocess.run(
                    ["xdotool", "getwindowname", window_id],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                window_title = (
                    name_result.stdout.strip() if name_result.returncode == 0 else ""
                )

                return {
                    "application": "Unknown",
                    "window_title": window_title,
                    "app_type": self._identify_app_type("", window_title),
                    "timestamp": datetime.now().isoformat(),
                }
        except Exception as e:
            print(f"Error getting active window on Linux: {e}")

        return {}

    def _identify_app_type(self, app_name: str, window_title: str) -> str:
        """Identify the type of application based on name and title"""
        app_lower = app_name.lower()
        title_lower = window_title.lower()

        # Excel detection
        if "excel" in app_lower or ".xlsx" in title_lower or ".xls" in title_lower:
            return "excel"

        # Google Sheets detection
        if "chrome" in app_lower or "safari" in app_lower or "firefox" in app_lower:
            if "sheets.google.com" in title_lower or "google sheets" in title_lower:
                return "google_sheets"

        # Tableau detection
        if "tableau" in app_lower or "tableau" in title_lower:
            return "tableau"

        # PowerPoint detection
        if "powerpoint" in app_lower or ".pptx" in title_lower or ".ppt" in title_lower:
            return "powerpoint"

        # Email detection
        if "outlook" in app_lower or "mail" in app_lower or "gmail" in title_lower:
            return "email"

        return "unknown"

    def get_all_open_windows(self) -> List[Dict[str, Any]]:
        """Get information about all open windows"""
        if self.system == "Darwin":  # macOS
            return self._get_all_windows_macos()
        elif self.system == "Windows":
            return self._get_all_windows_windows()
        elif self.system == "Linux":
            return self._get_all_windows_linux()
        return []

    def _get_all_windows_macos(self) -> List[Dict[str, Any]]:
        """Get all window information on macOS"""
        windows = []
        try:
            script = """
            tell application "System Events"
                set appList to every application process whose visible is true
                set windowInfo to {}
                
                repeat with appProc in appList
                    set appName to name of appProc
                    try
                        set windowNames to name of every window of appProc
                        repeat with winName in windowNames
                            set end of windowInfo to appName & "|" & winName
                        end repeat
                    end try
                end repeat
                
                return windowInfo
            end tell
            """

            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split(", ")
                for line in lines:
                    if "|" in line:
                        parts = line.split("|")
                        app_name = parts[0]
                        window_title = parts[1] if len(parts) > 1 else ""

                        windows.append(
                            {
                                "application": app_name,
                                "window_title": window_title,
                                "app_type": self._identify_app_type(
                                    app_name, window_title
                                ),
                            }
                        )
        except Exception as e:
            print(f"Error getting all windows on macOS: {e}")

        return windows

    def _get_all_windows_windows(self) -> List[Dict[str, Any]]:
        """Get all window information on Windows"""
        # This would require Windows-specific implementation
        return []

    def _get_all_windows_linux(self) -> List[Dict[str, Any]]:
        """Get all window information on Linux"""
        # This would require Linux-specific implementation
        return []

    def find_windows_by_type(self, app_type: str) -> List[Dict[str, Any]]:
        """Find all windows of a specific application type"""
        all_windows = self.get_all_open_windows()
        return [w for w in all_windows if w.get("app_type") == app_type]

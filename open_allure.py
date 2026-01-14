#!/usr/bin/env python3
"""
Script to open Allure report in browser with HTTP server
"""
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    # Paths
    report_dir = Path(__file__).parent / "reports" / "allure-report"
    
    if not report_dir.exists():
        print(f"❌ Allure report not found at {report_dir}")
        print("Run: python -m pytest")
        return
    
    # Start HTTP server in background
    print(f"🌐 Starting HTTP server for Allure report...")
    print(f"📁 Report directory: {report_dir}")
    
    # Change to report directory and start server
    os.chdir(report_dir)
    
    try:
        # Start server
        process = subprocess.Popen(
            ["/usr/bin/python3", "-m", "http.server", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(2)
        
        # Open in browser
        url = "http://localhost:8000"
        print(f"✅ Server started!")
        print(f"🌐 Opening {url} in browser...")
        
        webbrowser.open(url)
        
        print(f"\n✨ Allure report is now open!")
        print(f"Press Ctrl+C to stop the server\n")
        
        # Keep server running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n✋ Stopping server...")
        process.terminate()
        print("Done!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

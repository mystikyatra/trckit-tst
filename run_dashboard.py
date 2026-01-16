#!/usr/bin/env python3
"""
Truckit Automation Test Dashboard Runner

This script starts the Flask-based dashboard for viewing test results,
metrics, trends, and failure analysis.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import plotly
        import pandas
        print("✓ All dashboard dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install dependencies")
            return False

def start_dashboard():
    """Start the Flask dashboard application"""
    dashboard_dir = Path(__file__).parent / "dashboard"
    app_path = dashboard_dir / "app.py"

    if not app_path.exists():
        print(f"✗ Dashboard application not found at {app_path}")
        return False

    print("🚀 Starting Truckit Test Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the dashboard")
    print("-" * 50)

    try:
        # Change to dashboard directory and run the app
        os.chdir(dashboard_dir)
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start dashboard: {e}")
        return False

    return True

def main():
    """Main function"""
    print("🎯 Truckit Automation Test Dashboard")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path("dashboard").exists():
        print("✗ Please run this script from the project root directory")
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Start dashboard
    if not start_dashboard():
        sys.exit(1)

if __name__ == "__main__":
    main()
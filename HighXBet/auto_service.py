import schedule
import time
import subprocess
import sys
from datetime import datetime
import os

def run_bot():
    try:
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Auto-running bot...")
        os.chdir('C:\\HighXBet')
        subprocess.run([sys.executable, 'master_bot.py'], check=True)
    except Exception as e:
        print(f"❌ Error: {e}")

# Run at these times daily
schedule.every().day.at("09:00").do(run_bot)
schedule.every().day.at("17:00").do(run_bot)

print("🤖 HIGHXBET AUTO-SERVICE STARTED")
print("✅ Bot will run automatically at 9AM and 5PM daily")
print("💻 Running in background...")

# Keep running forever
while True:
    schedule.run_pending()
    time.sleep(60)
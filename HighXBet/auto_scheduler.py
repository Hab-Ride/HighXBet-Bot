import schedule
import time
import subprocess
from datetime import datetime

def run_bot():
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Running HighXBet Bot...")
    subprocess.run(['python', 'master_bot.py'])
    print(f"✅ {datetime.now().strftime('%H:%M')} - Analysis completed")

print("🤖 HIGHXBET AUTO-SCHEDULER")
print("=" * 50)
print("Bot will run automatically at:")
print("🕘 09:00 - Morning analysis")
print("🕛 12:00 - Lunch update") 
print("🕔 17:00 - Evening analysis")
print("=" * 50)

# Schedule runs
schedule.every().day.at("09:00").do(run_bot)
schedule.every().day.at("12:00").do(run_bot)
schedule.every().day.at("17:00").do(run_bot)

# Run once immediately
run_bot()

print("\n⏰ Scheduler active! Bot will run automatically.")
print("💻 Keep this window open.")
print("🛑 Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)
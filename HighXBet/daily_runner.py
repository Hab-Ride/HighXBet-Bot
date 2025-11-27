import schedule
import time
from datetime import datetime

def run_bot():
    """Run the master bot"""
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Running analysis...")
    
    # Import and run the master bot
    from master_bot import MasterBot
    bot = MasterBot()
    bot.run_complete_analysis()
    
    print(f"✅ Analysis completed at {datetime.now().strftime('%H:%M')}")

def main():
    print("📅 HIGHXBET DAILY SCHEDULER")
    print("=" * 50)
    print("Bot will run automatically at scheduled times!")
    print("Current schedule:")
    print("🕘 09:00 AM - Morning analysis") 
    print("🕛 12:00 PM - Lunchtime update")
    print("🕔 05:00 PM - Evening analysis")
    print("=" * 50)
    
    # Schedule the bot to run at specific times
    schedule.every().day.at("09:00").do(run_bot)
    schedule.every().day.at("12:00").do(run_bot) 
    schedule.every().day.at("17:00").do(run_bot)
    
    # Also run once immediately
    run_bot()
    
    print("\n⏰ Scheduler started! Bot will run automatically.")
    print("💡 Keep this window open for automated analysis.")
    print("🛑 Press Ctrl+C to stop the scheduler.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user.")
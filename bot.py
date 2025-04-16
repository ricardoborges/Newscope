import os
import time
import schedule
import logging
import threading
import datetime
from dotenv import load_dotenv
from newsbot import NewsBot

from telegram.ext import (
    Application,
    CommandHandler,
)
from telegram import Update

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Initialize bot with token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
news_bot = None

def run_scheduler():
    """Run the scheduler in a separate thread"""
    logger.info("Scheduler thread started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            time.sleep(60)  # Wait before retry

def schedule_collect():
    global news_bot
    logger.info("Running scheduled news collection")
    news_bot.collect_and_send_news()
        
def main():
    global news_bot
    
    if not TELEGRAM_TOKEN:
        raise ValueError("Token do bot não encontrado. Defina TELEGRAM_TOKEN no .env.")

    # Initialize the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()    
    
    # Initialize NewsBot with the token
    news_bot = NewsBot(telegram_token=TELEGRAM_TOKEN)
    
    # Add command handlers
    application.add_handler(CommandHandler("start", news_bot.start_command))
    application.add_handler(CommandHandler("hoje", news_bot.today_command))
    application.add_handler(CommandHandler("sair", news_bot.sair_command))
    application.add_handler(CommandHandler("feed", news_bot.feed))

    # Schedule tasks
    #schedule.every().day.at("12:08").do(schedule_collect)

    #for hour in range(7, 22):
    #    schedule.every().day.at(f"{hour:02d}:00").do(schedule_collect)
    #    schedule.every().day.at(f"{hour:02d}:30").do(schedule_collect)



    # For testing, uncomment to run every 5 minutes
    # schedule.every(5).minutes.do(schedule_collect)
  
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("Scheduler started")

    # Start the bot
    logger.info("Bot iniciado. Aguardando comandos...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

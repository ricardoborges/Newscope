import logging
from feed.news_collector import NewsCollector
from repository.firebase_news_repository import FirebaseNewsRepository
from repository.users_repository import UsersRepository

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from services.telegram import Telegram

logger = logging.getLogger(__name__)

class NewsBot:
    def __init__(self, telegram_token: str):
        self.telegram = Telegram(token=telegram_token)
        self.news_repository = FirebaseNewsRepository()
        self.users_repository = UsersRepository()
        self.collector = NewsCollector(self.news_repository)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - register user"""
        chat_id = update.effective_chat.id
        if not self.users_repository.user_exists(chat_id):
            self.users_repository.save_user(chat_id)
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Você foi registrado para receber atualizações de notícias."
            )
            logger.info(f"New user registered: {chat_id}")
        else:
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Você já está registrado para receber atualizações de notícias."
            )
            logger.info(f"Existing user connected: {chat_id}")

    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /hoje command - send today's news"""
        chat_id = update.effective_chat.id
        today_news = self.news_repository.get_today_news()
        if today_news:
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Encontrei {len(today_news)} notícias de hoje:"
            )
            for news_item in today_news:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"📰 *{news_item['title']}*\n{news_item['url']}",
                    parse_mode="Markdown"
                )
        else:
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Não há notícias para hoje ainda."
            )
        
    def send_news_to(self, chat_id, news_item):
        """Send a news item to a specific user."""
        try:
            self.telegram.send_message(
                chat_id=chat_id,
                message=f"📰 *{news_item['title']}*\n{news_item['url']}",
                parse_mode="Markdown"
            )
            logger.info(f"Sent news to user {chat_id}: {news_item['title']}")
        except Exception as e:
            logger.error(f"Failed to send news to {chat_id}: {str(e)}")

    def collect_and_send_news(self):
        """Collect news and send to all registered users."""
        logger.info("Starting news collection")
        try:
            self.collector.run()
            unprocessed_news = self.news_repository.get_unprocessed_news()
            logger.info(f"Found {len(unprocessed_news)} unprocessed news items")
            
            users = self.users_repository.get_all_chat_ids()

            for news_item in unprocessed_news:
                logger.info(f"Sending news item: {news_item['title']}")
                for chat_id in users:
                    self.send_news_to(chat_id, news_item)

                self.news_repository.update_news(news_item['id'], {'processed': True})
            logger.info("News collection and distribution completed")
        except Exception as e:
            logger.error(f"Error in collect_and_send_news: {str(e)}")
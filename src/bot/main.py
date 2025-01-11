import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, JobQueue
from .bot_config import TG_BOT_TOKEN, TIMEZONE
from .constants import WELCOME_MESSAGE
from .handlers.message import MessageProcessor
from contextlib import asynccontextmanager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.message_processor = MessageProcessor()
        
    async def start(self, update: Update, context):
        await update.message.reply_text(WELCOME_MESSAGE)
        
    async def handle_message(self, update: Update, context):
        try:
            response = await self.message_processor.process_message(update, context)
            if response:
                await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            await update.message.reply_text("Sorry, there was an error processing your message.")
            
    def run(self):
        # Build application
        application = (
            Application.builder()
            .token(TG_BOT_TOKEN)
            .build()
        )
        
        # Create and set JobQueue
        job_queue = application.job_queue
        job_queue.scheduler.configure(timezone=TIMEZONE)
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, 
                self.handle_message
            )
        )
        application.add_handler(
            MessageHandler(
                filters.VOICE | filters.PHOTO | filters.DOCUMENT, 
                self.handle_message
            )
        )
        
        # Add shutdown handler
        application.add_error_handler(self._handle_error)
        
        # Run bot
        application.run_polling()
        
    async def _handle_error(self, update: Update, context):
        """Log errors caused by Updates."""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
        
    async def shutdown(self):
        """Cleanup resources"""
        await self.message_processor.close()

def main():
    bot = TelegramBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {str(e)}", exc_info=True)
    finally:
        asyncio.run(bot.shutdown())

if __name__ == '__main__':
    main()

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import ccxt
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot with your token from BotFather
updater = Updater(token=' 6752279701:AAExNXnB5VKFOqfuA9XNu3I2tduBUVqCrbY ', use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Monitoring crypto volume surges...')
    context.bot_data.setdefault('subscribers', set()).add(update.message.chat_id)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def check_volume_surge() -> bool:
    # Initialize the exchange API
    exchange = ccxt.binance()  # Example with Binance
    pair = 'BTC/USDT'  # Example pair
    timeframe = '1m'  # Timeframe for volume data
    limit = 5  # Number of recent data points to check

    # Fetch recent candlestick data
    candles = exchange.fetch_ohlcv(pair, timeframe, limit=limit)
    volumes = [candle[5] for candle in candles]  # Extract volumes

    # Detect a volume surge
    volume_surge_detected = volumes[-1] > 1.5 * sum(volumes[:-1]) / (limit - 1)
    return volume_surge_detected

    def alert_users(context: CallbackContext) -> None:
     if check_volume_surge():
        for user_id in amayelwabot.bot_data['subscribers']:
            context.bot.send_message(chat_id=user_id, text="Volume surge detected!")

job_queue = updater.job_queue
job_queue.run_repeating(alert_users, interval=60, first=0)  # Check every minute

updater.start_polling()
updater.idle()  # Run the bot until you press Ctrl-C
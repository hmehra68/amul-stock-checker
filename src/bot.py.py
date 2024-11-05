import logging
from telegram.ext import Application, CommandHandler
import requests
from bs4 import BeautifulSoup
import asyncio
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
PRODUCT_URL = 'https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30'
CHAT_ID = 'YOUR_CHAT_ID'
CHECK_INTERVAL = 300  # 5 minutes

class AmulStockCheckerBot:
    def __init__(self):
        self.previous_status = False
        self.running = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://shop.amul.com/',
            'Origin': 'https://shop.amul.com'
        })

    async def start(self, update, context):
        """Handler for /start command"""
        if not self.running:
            self.running = True
            await update.message.reply_text('Started monitoring Amul High Protein Rose Lassi stock! You will be notified when it becomes available.')
            await self.check_stock_periodically(context)
        else:
            await update.message.reply_text('Stock checker is already running!')

    async def stop(self, update, context):
        """Handler for /stop command"""
        self.running = False
        await update.message.reply_text('Stock checker stopped!')

    async def check_stock_periodically(self, context):
        """Periodically checks stock status"""
        while self.running:
            try:
                stock_info = self.check_stock()
                if stock_info['in_stock'] and not self.previous_status:
                    message = (
                        f"🥛 Amul High Protein Rose Lassi is now in stock! 🎉\n\n"
                        f"Price: {stock_info['price']}\n"
                        f"Quantity Available: {stock_info['quantity']}\n\n"
                        f"Buy now: {PRODUCT_URL}"
                    )
                    await context.bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,
                        disable_web_page_preview=False
                    )
                self.previous_status = stock_info['in_stock']
                
            except Exception as e:
                logging.error(f"Error checking stock: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)

    def check_stock(self):
        """
        Checks if Amul product is in stock
        Returns dict with stock info
        """
        try:
            # Extract product ID from URL
            product_id = PRODUCT_URL.split('/')[-1]
            
            # First, get the product details
            response = self.session.get(PRODUCT_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for the availability status
            stock_info = {
                'in_stock': False,
                'price': 'N/A',
                'quantity': 0
            }
            
            # Check for out of stock indicators
            out_of_stock_div = soup.find('div', class_='out-of-stock')
            if not out_of_stock_div:
                # If we don't find the out of stock div, product might be in stock
                price_element = soup.find('span', class_='price')
                if price_element:
                    stock_info['price'] = price_element.text.strip()
                
                # Try to find quantity available
                quantity_element = soup.find('div', class_='stock-qty')
                if quantity_element:
                    qty_text = quantity_element.text.strip()
                    try:
                        stock_info['quantity'] = int(''.join(filter(str.isdigit, qty_text)))
                    except ValueError:
                        stock_info['quantity'] = "Available"
                
                stock_info['in_stock'] = True
            
            return stock_info
            
        except Exception as e:
            logging.error(f"Error in check_stock: {e}")
            return {'in_stock': False, 'price': 'N/A', 'quantity': 0}

async def main():
    """Main function to run the bot"""
    bot = AmulStockCheckerBot()
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("stop", bot.stop))
    
    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
# Amul Stock Checker Bot

A Telegram bot that monitors Amul product availability and sends notifications when items come back in stock.

## Features

- Real-time stock monitoring for Amul products
- Telegram notifications when products become available
- Configurable checking intervals
- Detailed stock information including price and quantity
- Easy to deploy on various platforms

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Your Telegram Chat ID (from [@userinfobot](https://t.me/userinfobot))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/amul-stock-checker.git
cd amul-stock-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example config and fill in your details:
```bash
cp config.example.py config.py
```

4. Edit `config.py` with your Telegram bot token and chat ID.

## Usage

Run the bot locally:
```bash
python bot.py
```

Bot commands:
- `/start` - Start monitoring stock
- `/stop` - Stop monitoring stock

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions on various platforms.

## License

MIT License - see [LICENSE](LICENSE) file for details

import asyncio
from bot import Bot

bot = Bot()

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(bot.start())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
    finally:
        loop.run_until_complete(bot.stop())

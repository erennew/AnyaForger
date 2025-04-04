import asyncio
from bot import Bot

bot = Bot()

async def main():
    await bot.start()
    print("🤖 Bot is up and running!")
    await asyncio.Event().wait()  # Keeps the bot running forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("😴 Bot stopped.")

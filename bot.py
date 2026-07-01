import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import requests

# Set up logging to see what your bot is doing
logging.basicConfig(level=logging.INFO)

# Get your bot token from the environment variables set in Railway
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found! Set it in Railway environment variables.")

# Initialize the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Command Handlers ---

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """Handle /start and /help commands."""
    await message.reply(
        "👋 Hello! I'm your AI Icon Bot.\n\n"
        "Send me a prompt describing an icon you need, and I'll generate it for you.\n"
        "Example: 'a red apple icon' or 'a minimalist cat face'\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Show this message"
    )

@dp.message_handler()
async def generate_icon(message: types.Message):
    """Handle text messages: generate an icon from the prompt."""
    prompt = message.text
    await message.reply("🎨 Generating your icon... Please wait a moment.")

    try:
        # --- TODO: Choose your Image Generation Method ---
        # Option 1: Use an external API (e.g., Pollinations.ai, OpenAI DALL-E, etc.)
        # Option 2: Integrate with a local AI model using libraries like `diffusers`
        
        # Example using a simple public API (no API key needed for pollinations.ai)
        # Note: This is a simplified example. For production, handle errors and use async requests.
        response = requests.get(
            f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}",
            timeout=30
        )
        
        if response.status_code == 200:
            # Send the generated image back to the user
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=response.content,
                caption=f"✅ Here's your icon for: '{prompt}'"
            )
        else:
            await message.reply("❌ Sorry, I couldn't generate the icon. Please try again later.")
        
    except Exception as e:
        logging.error(f"Error generating icon: {e}")
        await message.reply("❌ An error occurred while generating your icon. Please try again later.")

# --- Main Execution ---
if __name__ == '__main__':
    # This starts the bot using long polling, which is ideal for Railway
    executor.start_polling(dp, skip_updates=True)

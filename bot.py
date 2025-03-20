import os
import asyncio
from telethon import TelegramClient, events
import subprocess
import random
import sys
from datetime import datetime

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WATERMARK_TEXT = "Telegram Id-@skillwithgaurav\nWebsite-Riyasmm.shop"
OUTPUT_FILENAME = "watermarked_video.mp4"
FONT_PATH = "arial.ttf"  # Ensure this font is available in the working directory

# Initialize Telegram client
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to generate dynamic watermark positions
def generate_drawtext():
    positions = [
        (50, 50),   # Top-left
        (300, 100), # Middle-top
        (100, 400), # Bottom-left
        (500, 500), # Bottom-right
        (150, 250)  # Center
    ]
    pos = random.choice(positions)
    return f"drawtext=text='{WATERMARK_TEXT}':x={pos[0]}:y={pos[1]}:fontsize=48:fontcolor=white@0.8:fontfile={FONT_PATH}:box=1:boxcolor=black@0.4:enable='lt(mod(t,5),5)'"

# Start command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(
        "👋 Hello! Send me a video, and I will add a professional watermark to it.\n\n"
        "⚡ Fast processing\n"
        "🎯 Dynamic watermark every 5 seconds\n"
        "🚀 Ready for Heroku!"
    )

# Handle incoming videos
@bot.on(events.NewMessage(incoming=True))
async def watermark_video(event):
    if event.video:
        try:
            await event.reply("🔄 Processing your video with a dynamic watermark...")

            # Download the video
            video_path = await event.download_media()
            output_path = OUTPUT_FILENAME

            # Generate FFmpeg command
            drawtext = generate_drawtext()
            cmd = [
                "ffmpeg",
                "-i", video_path,  # Input video
                "-vf", drawtext,   # Watermark filter
                "-preset", "ultrafast",  # Fast processing
                "-crf", "23",      # Quality level
                "-codec:a", "copy",  # Copy original audio
                output_path        # Output file
            ]

            # Run FFmpeg command with live progress
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()

            # Send the watermarked video
            await event.reply(
                "✅ Done! Here's your watermarked video.\n\n"
                f"📝 Watermark Text: {WATERMARK_TEXT}\n"
                "🔗 Visit: Riyasmm.shop",
                file=output_path
            )

        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
        finally:
            # Clean up temporary files
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(output_path):
                os.remove(output_path)

# Run the bot
print("🤖 Bot is running with LIVE progress log...")
bot.run_until_disconnected()

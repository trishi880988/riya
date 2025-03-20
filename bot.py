import os
import asyncio
from telethon import TelegramClient, events
import subprocess
import random
import sys

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WATERMARK_TEXT = "Join - @skillwithgaurav"

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("👋 Hello! Send me a video and I will add a watermark.\n\n⚡ Fast processing\n🎯 Dynamic watermark every 5 sec\n🚀 Ready for Koyeb!")

@bot.on(events.NewMessage(incoming=True))
async def watermark_video(event):
    if event.video:
        await event.reply("🔄 Processing your video with dynamic watermark...")
        
        video = await event.download_media()
        output = "watermarked.mp4"
        
        # Generate random position list
        positions = [(50,50), (300,100), (100,400), (500,500), (150,250)]
        pos = random.choice(positions)
        
        drawtext = f"drawtext=text='{WATERMARK_TEXT}':x={pos[0]}:y={pos[1]}:fontsize=24:fontcolor=white@0.8:box=1:boxcolor=black@0.4:enable='lt(mod(t,5),5)'"

        # FFmpeg command with speed optimizations
        cmd = [
            "ffmpeg", "-i", video,
            "-vf", drawtext,
            "-preset", "ultrafast",  # Fastest speed
            "-crf", "23",  # Quality level (lower = better)
            "-codec:a", "copy",
            output
        ]

        # Live progress print
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
        
        await event.reply("✅ Done! Here's your watermarked video:", file=output)
        
        os.remove(video)
        os.remove(output)

print("🤖 Bot is running with LIVE progress log...")
bot.run_until_disconnected()

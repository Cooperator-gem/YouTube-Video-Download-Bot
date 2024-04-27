from pyrogram import Client, filters
from pytube import YouTube
import asyncio

API_ID = "16393106"
API_HASH = "061fbf1aff7eecf2edb8434ddbab7a7d"
BOT_TOKEN = "7019653925:AAFtUsAz-2w3IglgY_tionN5qE6bkcr02F4"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    user = message.from_user
    message.reply_text(f"Hello, @{user.username}!\n\nSend me the YouTube link of the video you want to upload.\n\n👑OWNER👑 - @unknownpersonzz\n💫SUPPORT💫  - https://t.me/unknownpersonzz ")

@app.on_message(filters.command("help"))
def help(client, message):
    help_text = """
    Welcome to the YouTube Video Uploader Bot!

To upload a YouTube video, simply send me the YouTube link.
    
Enjoy using the bot!

   ©️ Channel : @unknownpersonzz
    """
    message.reply_text(help_text)

async def download_video(youtube_link, downloading_msg, quality='720p'):
    yt = YouTube(youtube_link)
    video = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()
    video.download(filename='downloaded_video.mp4')
    await downloading_msg.edit_text("Video downloaded successfully!")

async def upload_video(chat_id, uploading_msg):
    await uploading_msg.edit_text("Uploading video...")
    await app.send_video(chat_id, video=open('downloaded_video.mp4', 'rb'))

@app.on_message(filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    youtube_link = message.text
    try:
        # Downloading text message
        downloading_msg = await message.reply_text("Downloading video...")

        # Quality selection keyboard
        quality_keyboard = [
            ["144p", "240p", "360p"],
            ["480p", "720p", "1080p"]
        ]

        # Quality selection message
        quality_selection_msg = await message.reply_text("Select the video quality:", reply_markup={"keyboard": quality_keyboard, "resize_keyboard": True})

        # Wait for user to select quality
        selected_quality = await app.listen(filters=filters.text & filters.user(message.from_user.id))
        quality = selected_quality.text

        # Remove quality selection message
        await quality_selection_msg.delete()

        # Download the YouTube video with selected quality
        await download_video(youtube_link, downloading_msg, quality)

        # Uploading text message
        uploading_msg = await message.reply_text("Uploading video...")

        # Upload the video
        await upload_video(message.chat.id, uploading_msg)

        # Delay for a few seconds and delete downloading and uploading messages
        await asyncio.sleep(2)
        await downloading_msg.delete()
        await uploading_msg.delete()

        # Send successful upload message
        await message.reply_text("\n\nOWNER : @unknownpersonzz 💕\n\nSUCCESSFULLY UPLOADED!")

    except Exception as e:
        error_text = 'Error: Failed to process the YouTube link. Please make sure the link is valid and try again.'
        await message.reply_text(error_text)

print("🎊 I AM ALIVE 🎊")
app.run()

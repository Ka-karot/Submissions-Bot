import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyromod import listen

TOKEN = os.environ.get('TOKEN')
ID = os.environ.get('ID')
HASH = os.environ.get('HASH')
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', "Anime_Memes_XD")
CHANNEL_ID = os.environ.get('CHANNEL_ID', -1001409286430)
BANNED_LIST = []
bot = Client('bot',api_id=ID,api_hash=str(HASH),bot_token=str(TOKEN))
buttoms = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Approve", callback_data="approve"
            ),
            InlineKeyboardButton(
                text="Disapprove", callback_data="dis"
            ),
        ],
    ]
)

@bot.on_message(filters.text & filters.private)
async def start(client, message):
    text = f"Hello {message.from_user.mention},\nI am a Meme Submittor [Bot](https://telegra.ph/file/b1026e0540bcda5090349.jpg) made for @Anime_Memes_XD\nSend Me the meme you wanna Submit"
    await message.reply_text(text=text)

@bot.on_message(filters.group & filters.command('start'))
async def ghello(_, message):
    message.reply_text("Please contact me in PM")

@bot.on_message(filters.photo & filters.private)
async def photo(client, message):
    try:
        file_id = message.photo.file_id
    except:
        bot.send_message(720518864, f"Cant retrieve File ID\nMessage by {message.from_user.mention}")
    caption = f"From: {message.from_user.mention}\nID: {message.from_user.id}"
    await bot.send_photo(-1001296688588, photo=file_id, caption=caption, reply_markup=buttoms)
    await message.reply_text("Ok, Sent To Admins, It will be posted after their Approval")

@bot.on_callback_query(filters.regex("approve"))
def approve(submission, query):
    sender = query.message.caption.split("ID: ")
    x = bot.send_photo(CHANNEL_ID, photo=query.message.photo.file_id, caption="#anime_meme")
    link = f"t.me/{CHANNEL_USERNAME}/{x.message_id}"
    query.answer("Kay Approved")
    query.edit_message_caption(f"This Meme Has been Approved by {query.from_user.mention}🙃\nUser: {sender[1]}",reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Post link  🔗", url= link)]]))
    bot.send_message(sender[1], text = f"[Your Meme](link) Has Been Approved.\nThank You for Submitting")

@bot.on_callback_query(filters.regex("dis"))
def disapprove(_, query):
    query.answer("Kay Disapproved")
    sender = query.message.caption.split("ID: ")
    bot.send_message(sender[1], text = f"I'm Sorry, but Your Meme has Been Disapproved by Some Admin")
    query.message.delete()

bot.run() 

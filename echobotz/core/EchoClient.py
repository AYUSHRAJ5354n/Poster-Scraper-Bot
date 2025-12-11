from pyrogram import Client
from pyrogram.enums import ParseMode
from config import Config
from .. import LOGGER

EchoBot = Client(
    "EchoBotz",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    parse_mode=ParseMode.HTML,
)

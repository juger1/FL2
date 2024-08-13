#(©)Rapid_Bots

import os
import logging
from logging.handlers import RotatingFileHandler

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "8754146"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "8b56a6989f6d04f6f4fe78133ade02fd")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5669934860"))

#Port
PORT = os.environ.get("PORT", "8080")

#permanent cloudflare file store url eg. https://filestore.rapidbots.workers.dev?start
FURL = os.environ.get("FURL", "https://filestore.rapidbots.workers.dev?start=")

#cloudflare permanent url eg. https://sk.tamilsk.workers.dev/
CURL = os.environ.get("CURL", "https://sk.tamilsk.workers.dev/")

#fast dl link if need set True else set false (must use capital T)
STREAM = os.environ.get("STREAM", "True")

#Auto delete feature if need set True else set false (must use capital T)
DELETE = os.environ.get("DELETE", "false")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://SkMedia:Tharunraj1828@cluster0.vbdxs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "tamilskmoviez2")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = lambda: int(os.environ.get("FORCE_SUB_CHANNEL", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#verified message
VERIFIED_MSG = os.environ.get("VERIFIED_MSG", "<b>You Are Successfully Verified ❤️‍🩹\n\nYou Can Get Any Files Without Verifiy Untill Next 12Hrs.\n\nNaruto Shippuden Tamil - https://t.me/+Q3fgiRFgEOViY2I1\n\nTamil Movies/Series - https://t.me/+lW8rqXwP8qQ0ODZl\n\nVijay Tv Serials/Shows - https://t.me/+Jk4hcVP8A-43ZjZl\n\nCWC Season 5 - https://t.me/+G3yps9kTPE04ZDFl\n\nTop Cooku Dupe Cooku - https://t.me/+jfivsh1ShrA0MTE1</b>")

#verify message
VERIFY_MSG = os.environ.get("VERIFY_MSG", "<b>You Are Successfully Verified ❤️‍🩹\n\nYou Can Get Any Files Without Verifiy Untill Next 12Hrs.\n\nNaruto Shippuden Tamil - https://t.me/+Q3fgiRFgEOViY2I1\n\nTamil Movies/Series - https://t.me/+lW8rqXwP8qQ0ODZl\n\nVijay Tv Serials/Shows - https://t.me/+Jk4hcVP8A-43ZjZl\n\nCWC Season 5 - https://t.me/+G3yps9kTPE04ZDFl\n\nTop Cooku Dupe Cooku - https://t.me/+jfivsh1ShrA0MTE1</b>")

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>👋🏻 нєℓℓo {first}\n\nɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.\n\n🄼🄰🄳🄴 🄱🅈 @Rapid_Bots</b>")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>👋🏻 нєℓℓo {first},\n\nYou Need To Join My Channels To Use This Bot 🤖.\n\nPlease Join This Channels 👇🏻 And Come Back Here...</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = lambda: True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "filesharingbot.txt"

FL_CHANNEL = int(os.environ.get("FL_CHANNEL", "-1002116723783"))

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

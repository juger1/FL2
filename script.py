#(©)Rapid_Bots

#permanent cloudflare file store url eg. https://filestore.rapidbots.workers.dev?start
FURL = os.environ.get("FURL", "https://filestore.rapidbots.workers.dev?start=")

#stream cloudflare permanent url eg. https://sk.tamilsk.workers.dev/
CURL = os.environ.get("CURL", "https://sk.tamilsk.workers.dev/")

#else verified message if verify false it work 
EVERIFY_MSG = os.environ.get("EVERIFY_MSG", "<b>Hello 👋🏻, You Need To Verify To Get Files, Open Below Bot For Verification. \n\nOpen @Sk_Verify_Bot & Start The Bot 👍</b>")

#verified message
VERIFIED_MSG = os.environ.get("VERIFIED_MSG", "<b>You Are Successfully Verified ❤️‍🩹\n\nYou Can Get Any Files Without Verifiy Untill Next 12Hrs.\n\nTamil Movies/Series - https://t.me/+lW8rqXwP8qQ0ODZl\n\nVijay Tv Serials/Shows - https://t.me/+Jk4hcVP8A-43ZjZl\n\nCWC Season 5 - https://t.me/+G3yps9kTPE04ZDFl\n\nTop Cooku Dupe Cooku - https://t.me/+jfivsh1ShrA0MTE1</b>")

#verify message
VERIFY_MSG = os.environ.get("VERIFY_MSG", "<b>Hello 👋🏻, You Need To Verify The Link To Get Files, Verification Will Be Expired After 12 Hours.\n\nif You Don't Know how To Verify. Click Below Button To See How To Verify The Link.</b>")

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>👋🏻 нєℓℓo {first}\n\nɪᴛ's ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.\n\n🄼🄰🄳🄴 🄱🅈 @Rapid_Bots</b>")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>👋🏻 нєℓℓo {first},\n\nYou Need To Join My Channels To Use This Bot 🤖.\n\nPlease Join This Channels 👇🏻 And Come Back Here...</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", """<b>@TamilSk_Moviez - {previouscaption}

👉 Subscribe Our YouTube Channel - https://youtube.com/@SkNetwork2021

❤️ Share With Friends ❤️👉</b>‌‌""")

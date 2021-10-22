from asyncio.queues import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic

from config import BOT_NAME as BN
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only

@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(" CHOCOBAR RELOADING...**\n#------████.   ████\n#----██.  ██^██.  ██\n#---██______s______██\n#----██______i_____██\n#-------██____m___██\n#----------██___i__██\n#-------------█████\n\nCHOCOBAR RELOADED DONE ")
    
    


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ !")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("▶Pᴀᴜsᴇ")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("Nᴏᴛʜɪɴɢ ᴛᴏ ᴘʟᴀʏ !")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("Rᴇsᴜᴍᴇ")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("Nᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ !")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("Sᴛᴏᴘ sᴛʀᴇᴀᴍɪɴɢ  ᴏ ʏᴇᴀʜ..")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("Nᴏᴛʜɪɴɢ ᴛᴏ sᴛʀᴇᴀᴍɪɴɢ !!")
    else:
        callsmusic.queues.task_done(message.chat.id)

        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )

        await message.reply_text("Sᴋɪᴘ ᴛʜᴇ sᴏɴɢ !")

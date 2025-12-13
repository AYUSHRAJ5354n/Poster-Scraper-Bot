from asyncio import sleep, gather
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait,
    MessageNotModified,
    MessageEmpty,
    ReplyMarkupInvalid,
    PhotoInvalidDimensions,
    WebpageCurlFailed,
    MediaEmpty,
    MediaCaptionTooLong,
)

try:
    from pyrogram.errors import FloodPremiumWait
except ImportError:
    FloodPremiumWait = FloodWait

from ...core.EchoClient import EchoBot, ParseMode
from ... import LOGGER


async def send_message(message, text, buttons=None, block=True, photo=None, **kwargs):
    disable_web_page_preview = kwargs.pop("disable_web_page_preview", True)
    disable_notification = kwargs.pop("disable_notification", True)

    try:
        if photo:
            try:
                if isinstance(message, int):
                    return await EchoBot.bot.send_photo(
                        chat_id=message,
                        photo=photo,
                        caption=text,
                        reply_markup=buttons,
                        disable_notification=disable_notification,
                        **kwargs,
                    )
                return await message.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=buttons,
                    quote=True,
                    disable_notification=disable_notification,
                    **kwargs,
                )
            except FloodWait as f:
                LOGGER.warning(str(f))
                if not block:
                    return str(f)
                await sleep(f.value * 1.2)
                return await send_message(message, text, buttons, block, photo, **kwargs)
            except MediaCaptionTooLong:
                return await send_message(
                    message,
                    text[:1024],
                    buttons,
                    block,
                    photo,
                    **kwargs,
                )
            except (PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty):
                LOGGER.error("Invalid photo dimensions or empty media", exc_info=True)
                return
            except Exception:
                LOGGER.error("Error while sending photo", exc_info=True)
                return

        if isinstance(message, int):
            return await EchoBot.bot.send_message(
                chat_id=message,
                text=text,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                reply_markup=buttons,
                **kwargs,
            )
        return await message.reply(
            text=text,
            quote=True,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=buttons,
            **kwargs,
        )

    except (FloodWait, FloodPremiumWait) as f:
        LOGGER.warning(str(f))
        if not block:
            return str(f)
        await sleep(f.value * 1.2)
        return await send_message(message, text, buttons, block, photo, **kwargs)
    except ReplyMarkupInvalid as rmi:
        LOGGER.warning(str(rmi))
        return await send_message(message, text, None, block, photo, **kwargs)
    except MessageEmpty:
        kwargs["parse_mode"] = ParseMode.DISABLED
        return await send_message(message, text, buttons, block, photo, **kwargs)
    except Exception as e:
        LOGGER.error(str(e), exc_info=True)
        return str(e)


async def edit_message(message, text, buttons=None, block=True, **kwargs):
    try:
        disable_web_page_preview = kwargs.pop("disable_web_page_preview", True)
        return await message.edit_text(
            text=text,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=buttons,
            **kwargs,
        )
    except (MessageNotModified, MessageEmpty):
        pass
    except ReplyMarkupInvalid as rmi:
        LOGGER.warning(str(rmi))
        return await edit_message(message, text, None, block, **kwargs)
    except (FloodWait, FloodPremiumWait) as f:
        LOGGER.warning(str(f))
        if not block:
            return str(f)
        await sleep(f.value * 1.2)
        return await edit_message(message, text, buttons, block, **kwargs)
    except Exception as e:
        LOGGER.error(str(e), exc_info=True)
        return str(e)


async def edit_reply_markup(message, buttons):
    try:
        return await message.edit_reply_markup(reply_markup=buttons)
    except MessageNotModified:
        pass
    except (FloodWait, FloodPremiumWait) as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await edit_reply_markup(message, buttons)
    except Exception as e:
        LOGGER.error(str(e), exc_info=True)
        return str(e)


async def send_file(message, file, caption="", buttons=None, **kwargs):
    try:
        if isinstance(message, int):
            return await EchoBot.bot.send_document(
                chat_id=message,
                document=file,
                caption=caption,
                disable_notification=True,
                reply_markup=buttons,
                **kwargs,
            )
        return await message.reply_document(
            document=file,
            caption=caption,
            quote=True,
            disable_notification=True,
            reply_markup=buttons,
            **kwargs,
        )
    except (FloodWait, FloodPremiumWait) as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await send_file(message, file, caption, buttons, **kwargs)
    except Exception as e:
        LOGGER.error(str(e), exc_info=True)
        return str(e)


async def delete_message(*args):
    tasks = [msg.delete() for msg in args if isinstance(msg, Message)]
    if not tasks:
        return
    results = await gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            LOGGER.error(result)

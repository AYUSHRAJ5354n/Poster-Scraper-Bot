from pyrogram.enums import ChatType
from .. import LOGGER
from ..eco import echo
from ..helper.ott import _extract_url_from_message, _fetch_ott_info
from ..helper.utils.btns import EchoButtons
from ..helper.utils.msg_util import send_message, edit_message
from ..helper.utils.xtra import _task


@_task
async def _poster_cmd(client, message):
    try:
        if message.chat.type not in (
            ChatType.PRIVATE,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ):
            return

        cmd = message.command[0].split("@")[0].lstrip("/")
        target = _extract_url_from_message(message)

        if not target:
            return await send_message(message, "<b>Usage:</b>\n" f"/{cmd} &lt;ott-url&gt;  <i>or</i>\n" f"Reply to a URL with <code>/{cmd}</code>")
        wait = await send_message(message, f"<i>Fetching poster for:</i>\n<code>{target}</code>")
        info, err = await _fetch_ott_info(cmd, target)
        if err:
            return await edit_message(wait, f"<b>Error:</b> <code>{err}</code>")

        header = [
            f"<b>📺 Source:</b> {info['source']}",
            f"<b>🎬 Title:</b> {info['title']}",
            f"<b>📅 Year:</b> {info['year']}",
            "",
            "<b>✺ Original Input:</b>",
            f"<code>{target}</code>",
        ]

        poster_lines = []
        if info["landscape"]:
            poster_lines.append(
                f"• Landscape: <a href=\"{info['landscape']}\">Click Here</a>"
            )
        if info["poster"] and info["poster"] != info["landscape"]:
            poster_lines.append(
                f"• Portrait: <a href=\"{info['poster']}\">Click Here</a>"
            )

        text = (
            "\n".join(header)
            + "\n\n<b>⧉ Posters:</b>\n"
            + ("\n".join(poster_lines) if poster_lines else "• No posters found.")
            + "\n\n<blockquote>Bot By ➤ @NxTalks</blockquote>"
        )

        btns = EchoButtons()
        btns.url_button(echo.UP_BTN, echo.UPDTE)
        btns.url_button(echo.ST_BTN, echo.REPO)

        await edit_message(
            wait,
            text,
            buttons=btns.build(2),
            disable_web_page_preview=False,
        )

    except Exception as e:
        LOGGER.error(f"poster_cmd error: {e}", exc_info=True)
        await send_message(message, "<b>Error:</b> Something went wrong.")

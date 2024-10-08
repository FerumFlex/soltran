from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode, ChatAction
from telegram import LinkPreviewOptions

from logger import logger  # noqa

from config import settings
# from chain import run_agent
from multi_agent import run_agent
from tools import utils


HELP = """
Welcome to SolTran! 🌟

Explore the Solana blockchain with ease using our comprehensive suite of tools. Get started by choosing one of the following options:

You can ask whatever you want in free form, please add transaction id, wallet address, token id, or smart contract address to get more detailed information.

"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_html(
        HELP,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html(HELP)


async def run_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id,
        action=ChatAction.TYPING,
    )

    response = await run_agent(update.message.text)

    response = utils.format_solana_addresses(response)

    await update.message.reply_text(
        response,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.telegram_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run_chain))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# Auto Translategram

Auto Translategram is a Python package that provides translation capabilities for Telegram bots. It uses and supports multiple translation services.

## Installation

You can install Auto Translategram using pip:

```
pip install translategram
```

## Usage

### First you need to add a parameter to your handler called whatever you want *(in this example we called it ```message```)* and its type should be the ```string```.
```python
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(
            chat_id=update.effective_chat.id if update.effective_chat else 0,
            text=message
            )
```

### And then you need to call ```handler_translator``` method when you register your handler in handler class.
```python
login_handler = CommandHandler('login', translator.handler_translator(login, message="Welcome to our community!"))
```

### As well as you should create translator instance based on the framework you are using *(in this case python-telegram-bot)*.

```python
from auto_translategram import PythonTelegramBotTranslator, MtranslateTranslatorService

translator = PythonTelegramBotTranslator(MtranslateTranslatorService)
```

### And finally your file should looks like this:

```python
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from auto_translategram import PythonTelegramBotTranslator, MtranslateTranslatorService

translator = PythonTelegramBotTranslator(MtranslateTranslatorService)
TOKEN = 'YOUR_TOKEN'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(
            chat_id=update.effective_chat.id if update.effective_chat else 0,
            text=message
            )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(
            chat_id=update.effective_chat.id if update.effective_chat else 0,
            text=message
            )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    login_handler = CommandHandler('login', translator.handler_translator(login, message="Welcome to our community!"))
    start_handler = CommandHandler('start', translator.handler_translator(start, message="This bot is very simple. You can just login with the /login command and that is it!"))
    application.add_handler(login_handler)
    application.add_handler(start_handler)

    application.run_polling()

```

## TODO

* Implement cache system
    - Create abstract base class for different cache systems.
    - Cache System with Pickling and serialization (e.g. JSON).
        - The Pickle module in Python can be used to serialize dataclasses and store them on disk. This approach is simple and suitable for small to medium-sized projects.
    - Cache System with Memcache.
    - Cache System with Redis.
* Add aiogram framework adapter.
* Add pyTelegramBotApi framework adapter.
* Add support for more translation services.


## License

This project is licensed under the terms of the MIT license.
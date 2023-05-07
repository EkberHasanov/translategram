import inspect
from typing import Any, Coroutine, Callable
from telegram.ext import ContextTypes
from telegram import Update
from ..auto_translategram.translator_services import TranslatorService
from ..auto_translategram.translator import Translator


class PythonTelegramBotAdapter(Translator):
    """
    A Translator adapter for the python-telegram-bot framework.

    Inherits from the abstract class `Translator` and implements its `handler_translator` method
    to provide translation functionality for the python-telegram-bot framework.

    :param translator_service: The `TranslatorService` to use for translations.
    """

    def __init__(self, translator_service: TranslatorService):
        """
        Initializes a new PythonTelegramBotAdapter instance using the specified `translator_service`.

        :param translator_service: The `TranslatorService` to use for translations.
        """
        self._translator_service = translator_service()

    def handler_translator(
            self,
            func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], None],
            message: str) -> Callable[[Update, ContextTypes.DEFAULT_TYPE, str], Coroutine[Any, Any, Any]]:
        """
        A decorator that wraps a python-telegram-bot `handler` function to provide translation functionality.

        The decorated function will be executed after being wrapped with a new function that translates
        the incoming message into the user's preferred language (if it is not already in that language).
        If the user does not have a preferred language set or if it is set to 'en', the message will not be translated.

        :param func: The handler function that is used for handling commands by the Python-telegram-bot framework.
        :param message: The message to translate.
        :return: A coroutine that wraps the handler function and provides translation functionality.
        """

        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = message) -> Any:
            user_lang = update.effective_user.language_code if update.effective_user else 'en'
            message = message
            if user_lang != 'en' and user_lang is not None:
                message = await self._translator_service.translate_str(
                    text=message,
                    target_language=user_lang,
                    source_language='en'
                    )
            is_async = inspect.iscoroutinefunction(func)
            result = (await func(update, context, message)) if is_async else func(update, context, message)
            return result

        return wrapper

from abc import abstractmethod
import inspect
from typing import Any, Coroutine, Callable, Type, Union
from telegram.ext import ContextTypes

from telegram import Update

from translategram.translategram.cache import Cache
from translategram.translategram.translator_services import TranslatorService
from translategram.translategram.translator import Translator


class PythonTelegramBotAdapter(Translator):
    """
    A Translator adapter for the python-telegram-bot framework.

    Inherits from the abstract class `Translator` and implements its `handler_translator` method
    to provide translation functionality for the python-telegram-bot framework.
    """

    def __init__(
        self,
        translator_service: Type[TranslatorService],
        cache_system: Union[Type[Cache], None] = None,
    ) -> None:
        """
        Initializes a new PythonTelegramBotAdapter instance using the specified `translator_service`.

        :param translator_service: The `TranslatorService` to use for translations.
        :param cache_system: The cache system to be used for caching translations. If None, caching is disabled.
        """
        self._translator_service = translator_service()
        self._cache_system = cache_system

    def handler_translator(
        self, message: str, source_lang: str = "auto"
    ) -> Callable[
        [Callable[[Any, Any, str], object]],
        Callable[[Any, Any, str], Coroutine[Any, Any, Any]],
    ]:
        """
        A decorator that wraps a python-telegram-bot `handler` function to provide translation functionality.

        The decorated function will be executed after being wrapped with a new function that translates
        the incoming message into the user's preferred language (if it is not already in that language).

        :param message: The message to translate.
        :return: A coroutine that wraps the handler function and provides translation functionality.
        """

        def decorator(
            func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object]
        ) -> Callable[[Any, Any, str], Coroutine[Any, Any, Any]]:
            """
            Decorator function that provides translation functionality to a Python-telegram-bot `handler` function.

            :param func: The handler function that is used for handling commands by the Python-telegram-bot framework.
            :return: A coroutine that wraps the handler function and provides translation functionality.
            """

            async def wrapper(
                update: Update,
                context: ContextTypes.DEFAULT_TYPE,
                message: str = message,
            ) -> Any:
                user_lang = (
                    update.effective_user.language_code
                    if update.effective_user
                    else "en"
                )
                message = message
                msg = message
                if user_lang is not None:
                    if self._cache_system is not None:
                        msg = await self._cache_system.retrieve(
                            key=func.__name__ + "_" + user_lang
                        )  # type: ignore
                        if msg is None:
                            msg = await self._translator_service.translate_str(
                                text=message,
                                target_language=user_lang,
                                source_language=source_lang,
                            )
                            await self._cache_system.store(
                                key=func.__name__ + "_" + user_lang, value=msg
                            )  # type: ignore
                    else:
                        msg = await self._translator_service.translate_str(
                            text=message,
                            target_language=user_lang,
                            source_language=source_lang,
                        )
                is_async = inspect.iscoroutinefunction(func)
                if is_async:
                    result = await func(update, context, str(msg))  # type: ignore[misc]
                else:
                    result = func(update, context, str(msg))  # type: ignore[misc]
                return result

            return wrapper

        return decorator

    def dynamic_handler_translator(
        self, message_func: Callable[..., str], **params: dict
    ) -> Callable[
        [Callable[..., object]], Callable[[Any, Any, str], Coroutine[Any, Any, Any]]
    ]:
        def decorator(
            func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object]
        ) -> Callable[[Any, Any, str], Coroutine[Any, Any, Any]]:
            async def wrapper(
                update: Update,
                context: ContextTypes.DEFAULT_TYPE,
                message: str = message,
            ):
                ...

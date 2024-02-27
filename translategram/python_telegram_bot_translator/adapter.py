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

    async def _get_message_from_cache(
        self,
        func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object],
        user_lang: str,
        message: str,
        source_lang: str,
    ) -> str:
        """
        Gets the message from the cache system.

        :param func: The handler function that is used for handling commands by the Python-telegram-bot framework.
        :param user_lang: The language to translate the message to.
        :param message: The message to translate.
        :param source_lang: The language to translate the message from.
        :return: The message from the cache system.
        """
        msg = await self._cache_system.retrieve(
            key=func.__name__ + "_" + user_lang
            ) if self._cache_system is not None else ""  # type: ignore
        if msg is None or msg == "":
            msg = await self._translator_service.translate_str(
                text=message,
                target_language=user_lang,
                source_language=source_lang,
            )
            await self._cache_system.store(
                key=func.__name__ + "_" + user_lang, value=msg
            ) if self._cache_system is not None else ""  # type: ignore
        return msg

    async def _get_translated_message(
        self,
        user_lang: str,
        message: str,
        func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object],
        source_lang: str,
    ) -> str:
        """
        Gets the translated message for the specified `user_lang` and `message`.

        :param user_lang: The language to translate the message to.
        :param message: The message to translate.
        :param func: The handler function that is used for handling commands by the Python-telegram-bot framework.
        :param source_lang: The language to translate the message from.
        :return: The translated message.
        """
        msg = message
        if self._cache_system is not None:
            msg = await self._get_message_from_cache(
                func, user_lang, message, source_lang
            )
        return msg

    async def _return_handler_function(
        self,
        func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object],
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        message: str,
    ) -> Any:
        """
        Returns the handler function.

        :param func: The handler function that is used for handling commands by the Python-telegram-bot framework.
        :param update: The update object.
        :param context: The context object.
        :param message: The message to translate.
        :return: The handler function's result.
        """
        if inspect.iscoroutinefunction(func):
            return await func(update, context, message)
        return func(update, context, message)

    async def _get_user_language(self, update: Update) -> str:
        """
        Gets the user's language.

        :param update: The update object.
        :return: The user's language.
        """
        user_lang = (
            update.effective_user.language_code if update.effective_user else "en"
        )
        return str(user_lang)

    async def _get_message_func_result(
        self,
        message_func: Callable[[str, Update], str],
        user_inp: str,
        update: Union[Update, None] = None,
    ) -> str:
        if update:
            return str(
                await message_func(user_inp, update)
                if inspect.iscoroutinefunction(message_func)
                else message_func(user_inp, update)
            )
        return str(
            await message_func(user_inp)  # type: ignore
            if inspect.iscoroutinefunction(message_func)
            else message_func(user_inp)  # type: ignore
        )

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
                user_lang = await self._get_user_language(update=update)
                message = await self._get_translated_message(
                    user_lang=str(user_lang),
                    message=message,
                    func=func,
                    source_lang=source_lang,
                )
                return await self._return_handler_function(
                    func=func, update=update, context=context, message=message
                )

            return wrapper

        return decorator

    def dynamic_handler_translator(
        self,
        message_func: Callable[[str, Any], str],
        source_lang: str = "auto",
    ) -> Callable[
        [Callable[..., object]], Callable[[Any, Any], Coroutine[Any, Any, Any]]
    ]:
        def decorator(
            func: Callable[[Update, ContextTypes.DEFAULT_TYPE, str], object]
        ) -> Callable[[Any, Any], Coroutine[Any, Any, Any]]:
            async def wrapper(
                update: Update,
                context: ContextTypes.DEFAULT_TYPE,
            ) -> Any:
                user_inp = " ".join(context.args) if context.args else ""
                args = [user_inp]
                if type(update) in inspect.get_annotations(message_func).values():
                    args.append(update)  # type: ignore
                message = await self._get_message_func_result(message_func, *args)  # type: ignore
                user_lang = await self._get_user_language(update=update)
                message = await self._get_translated_message(
                    user_lang=user_lang,
                    message=message,
                    func=func,
                    source_lang=source_lang,
                )
                return await self._return_handler_function(
                    func=func, update=update, context=context, message=message
                )

            return wrapper

        return decorator

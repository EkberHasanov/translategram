import asyncio
from pathlib import Path
from collections.abc import Generator
import os
from typing import Any, Callable, Coroutine, Type
from unittest.mock import MagicMock
import pytest
from telegram import Update
from telegram.ext import ContextTypes
from translategram.translategram.translator import Translator
from translategram.translategram.translator_services import (
    TranslatorService,
    MtranslateTranslatorService,
)
from translategram.translategram.service_libs import mtranslate
from translategram.python_telegram_bot_translator.adapter import (
    PythonTelegramBotAdapter,
)
from translategram.translategram.cache import PickleCache


class CacheData:
    ...


@pytest.fixture
def cache(tmp_path: Path) -> Generator:
    obj = CacheData()
    cache: PickleCache = PickleCache(obj, filename=str(tmp_path / "translation.data"))
    yield cache
    os.remove(cache.pickle_file)


@pytest.fixture
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mtranslate_service() -> TranslatorService:
    return MtranslateTranslatorService()


@pytest.fixture
def mtranslate_object() -> Type[TranslatorService]:
    return MtranslateTranslatorService


@pytest.fixture
def mtranslate_lib() -> object:
    return mtranslate


@pytest.fixture
def mock_translator_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def adapter(mtranslate_object: Type[TranslatorService]) -> Translator:
    return PythonTelegramBotAdapter(mtranslate_object)


@pytest.fixture
def adapter_with_mock(mock_translator_service):
    return PythonTelegramBotAdapter(mock_translator_service)


@pytest.fixture
def update() -> Update:
    return Update(None, None)  # type: ignore


@pytest.fixture
def context() -> Type[ContextTypes.DEFAULT_TYPE]:
    return ContextTypes.DEFAULT_TYPE


@pytest.fixture
def message() -> str:
    return "Hello World"


@pytest.fixture
def handler_func() -> Callable:
    def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        return message

    return handler


@pytest.fixture
def translate_function() -> Callable[[str], str]:
    def tr_func(user_input: str) -> str:
        if len(user_input) > 10:
            return "Greater than 10"
        return "Less than 10"

    return tr_func


@pytest.fixture
def async_translate_function() -> Callable[[str], Coroutine[Any, Any, str]]:
    async def tr_func(user_input: str) -> str:
        if len(user_input) > 10:
            return "Greater than 10"
        return "Less than 10"

    return tr_func

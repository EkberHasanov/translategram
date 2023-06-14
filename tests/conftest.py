import asyncio
from pathlib import Path
from collections.abc import Generator
import os
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
def mtranslate_object() -> TranslatorService:
    return MtranslateTranslatorService


@pytest.fixture
def mtranslate_lib() -> mtranslate:
    return mtranslate


@pytest.fixture
def mock_translator_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def adapter(mtranslate_object: TranslatorService) -> Translator:
    return PythonTelegramBotAdapter(mtranslate_object)


@pytest.fixture
def adapter_with_mock(mock_translator_service):
    return PythonTelegramBotAdapter(mock_translator_service)


@pytest.fixture
def update() -> Update:
    return Update(None, None)


@pytest.fixture
def context() -> ContextTypes.DEFAULT_TYPE:
    return ContextTypes.DEFAULT_TYPE


@pytest.fixture
def message() -> str:
    return "Hello World"


@pytest.fixture
def handler_func() -> str:
    def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        return message

    return handler

import asyncio
from unittest.mock import MagicMock
import pytest
from telegram import Update
from telegram.ext import ContextTypes
from ..auto_translategram.translator_services import TranslatorService, MtranslateTranslatorService
from ..auto_translategram.service_libs import mtranslate
from ..python_telegram_bot_translator.adapter import PythonTelegramBotAdapter


@pytest.fixture
def event_loop():
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
def adapter(mtranslate_object):
    return PythonTelegramBotAdapter(mtranslate_object)


@pytest.fixture
def adapter_with_mock(mock_translator_service):
    return PythonTelegramBotAdapter(mock_translator_service)


@pytest.fixture
def update():
    return Update(None, None)


@pytest.fixture
def context():
    return ContextTypes.DEFAULT_TYPE


@pytest.fixture
def message() -> str:
    return "Hello World"


@pytest.fixture
def handler_func():
    def handler(update, context, message):
        return message
    return handler

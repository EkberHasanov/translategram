from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, Type, TypeVar, Union

from translategram.translategram.cache import Cache
from translategram.translategram.translator_services import TranslatorService

T = TypeVar("T")


class Translator(ABC):
    """
    Abstract base class for implementing translation functionality in various frameworks.
    This class provides a uniform interface for translation, allowing adapters to be written for different frameworks.
    This class is meant to be subclassed, and the `handler_translator` method should be implemented in the subclass.
    """

    def __init__(
        self,
        translator_service: TranslatorService,
        cache_system: Union[Type[Cache], None] = None,
    ) -> None:
        """
        Initializes a new Translator instance using the specified `translator_service`.

        :param translator_service: The `TranslatorService` to use for translations.
        :param cache_system: The cache system to be used for caching translations. If None, caching is disabled.
        """
        ...

    @abstractmethod
    def handler_translator(
        self, message: str, source_lang: str
    ) -> Callable[
        [Callable[..., object]], Callable[[Any, Any, str], Coroutine[Any, Any, Any]]
    ]:
        """
        Translate a message based on the users' language
        :param func: The handler function that is used for handling commands by Frameworks.
        :param message: The message to translate.
        """
        ...

    @abstractmethod
    def dynamic_handler_translator(
        self, message_func: Callable[[str, Any], str], source_lang: str = "auto"
    ) -> Callable[
        [Callable[..., object]], Callable[[Any, Any], Coroutine[Any, Any, Any]]
    ]:
        ...

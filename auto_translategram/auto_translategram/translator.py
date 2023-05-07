from abc import ABC, abstractmethod
from typing import Callable
from .translator_services import TranslatorService


class Translator(ABC):
    """
    Abstract base class for implementing translation functionality in various frameworks.
    This class provides a uniform interface for translation, allowing adapters to be written for different frameworks.
    This class is meant to be subclassed, and the `handler_translator` method should be implemented in the subclass.
    """
    def __init__(self, translator_service: TranslatorService) -> None:
        """
        Initializes a new Translator instance using the specified `translator_service`.

        :param translator_service: The `BaseTranslatorService` to use for translations.
        """
        ...

    @abstractmethod
    def handler_translator(self, func: Callable[..., None], message: str) -> Callable[..., None]:
        """
        Translate a message based on the users' language
        :param func: The handler function that is used for handling commands by Frameworks.
        :param message: The message to translate.
        """
        ...

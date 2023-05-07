from typing import Protocol
from .service_libs import mtranslate


class TranslatorService(Protocol):
    """
    Defines the interface for the translator services
    """
    async def translate_str(self, text: str, target_language: str = 'auto', source_language: str = 'auto') -> str:
        """
        Returns the translated string
        """
        ...


class MtranslateTranslatorService:
    """
    Implements the BaseTranslatorService protocol using the mtranslate library
    """
    def __init__(self) -> None:
        assert mtranslate, '`MtranslateTranslatorService` requires `mtranslate` package'
        self.service = mtranslate

    async def translate_str(self, text: str, target_language: str = 'auto', source_language: str = 'auto') -> str:
        """
        Returns the translated string using the mtranslate library
        """
        if not isinstance(text, str) or not isinstance(target_language, str) or not isinstance(source_language, str):
            raise TypeError('`text`, `target_language` and `source_language` must be a string')
        translated_text = self.service.translate(
            to_translate=text,
            to_language=target_language,
            from_language=source_language
            )
        return translated_text

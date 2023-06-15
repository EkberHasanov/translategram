from typing import Protocol
from translategram.translategram.service_libs import mtranslate


class TranslatorService(Protocol):
    """
    Defines the interface for the translator services
    """

    async def translate_str(
        self, text: str, target_language: str, source_language: str = "auto"
    ) -> str:
        """
        Translate the input string to the target language.

        :param text: The text to be translated.
        :param target_language: The target language code.
        :param source_language: The source language code. Default is 'auto'.
        :return: The translated string.
        """
        ...


class MtranslateTranslatorService:
    """
    Implements the BaseTranslatorService protocol using the mtranslate library
    """

    def __init__(self) -> None:
        """
        Initialize the `MtranslateTranslatorService` instance.

        :raises AssertionError: If the `mtranslate` package is not installed.
        """
        assert mtranslate, "`MtranslateTranslatorService` requires `mtranslate` package"
        self.service = mtranslate

    async def translate_str(
        self, text: str, target_language: str = "auto", source_language: str = "auto"
    ) -> str:
        """
        Translate the input string using the `mtranslate` library.

        :param text: The text to be translated.
        :param target_language: The target language code. Default is 'auto'.
        :param source_language: The source language code. Default is 'auto'.
        :return: The translated string.
        :raises TypeError: If `text`, `target_language`, or `source_language` is not a string.
        """
        if (
            not isinstance(text, str)
            or not isinstance(target_language, str)
            or not isinstance(source_language, str)
        ):
            raise TypeError(
                "`text`, `target_language` and `source_language` must be a string"
            )
        translated_text = self.service.translate(
            to_translate=text,
            to_language=target_language,
            from_language=source_language,
        )
        return str(translated_text)

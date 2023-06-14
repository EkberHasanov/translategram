import time
import pytest


async def mtranslate_translate_str_returns_str_test(mtranslate_service) -> None:
    text = "Hello World!"
    target_language = "es"
    source_language = "en"
    result = await mtranslate_service.translate_str(
        text, target_language, source_language
    )
    assert isinstance(result, str)


async def mtranslate_translate_str_without_source_returns_str_test(
    mtranslate_service,
) -> None:
    text = "Hello World!"
    target_language = "es"
    result = await mtranslate_service.translate_str(text, target_language)
    assert isinstance(result, str)


async def mtranslate_translate_str_with_source_test(mtranslate_service) -> None:
    text = "Hello World!"
    target_language = "es"
    source_language = "en"
    result = await mtranslate_service.translate_str(
        text, target_language, source_language
    )
    assert result == "¡Hola Mundo!"


async def mtranslate_translate_str_without_source_test(mtranslate_service) -> None:
    text = "Hello World!"
    target_language = "es"
    result = await mtranslate_service.translate_str(text, target_language)
    assert result == "¡Hola Mundo!"


async def mtranslate_translate_str_raises_error_on_invalid_input_test(
    mtranslate_service,
):
    with pytest.raises(TypeError) as exc_info:
        await mtranslate_service.translate_str(123, "en")
    assert (
        str(exc_info.value)
        == "`text`, `target_language` and `source_language` must be a string"
    )

    with pytest.raises(TypeError) as exc_info:
        await mtranslate_service.translate_str("Hello", 123)
    assert (
        str(exc_info.value)
        == "`text`, `target_language` and `source_language` must be a string"
    )

    with pytest.raises(TypeError) as exc_info:
        await mtranslate_service.translate_str("Hello", "es", 123)
    assert (
        str(exc_info.value)
        == "`text`, `target_language` and `source_language` must be a string"
    )


async def mtranslate_translate_str_handles_empty_string_test(
    mtranslate_service,
) -> None:
    result = await mtranslate_service.translate_str("", "es")
    assert result == ""


async def mtranslate_translate_str_handles_special_characters_test(
    mtranslate_service,
) -> None:
    special_chars_string = "Hello ~!@#$%^&*()_+ World"
    result = await mtranslate_service.translate_str(special_chars_string, "az")
    assert isinstance(result, str)
    assert result == "Salam ~!@#$%^&*()_+ Dünya"


async def mtranslate_translate_str_performance_test(mtranslate_service):
    text = "Hello World!" * 1000
    target_language = "es"

    num_runs = 5
    elapsed_times = []

    for i in range(num_runs):
        start_time = time.monotonic()
        await mtranslate_service.translate_str(text, target_language)
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        elapsed_times.append(elapsed_time)

    avg_elapsed_time = sum(elapsed_times) / num_runs
    max_elapsed_time = max(elapsed_times)
    print(f"Average elapsed time: {avg_elapsed_time:.2f} sec")
    print(f"Max elapsed time: {max_elapsed_time:.2f} sec")

    performance_threshold = 3
    assert (
        avg_elapsed_time < performance_threshold
    ), f"Average elapsed time exceeded threshold of {performance_threshold} sec"

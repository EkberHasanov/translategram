def init_test(adapter_with_mock, mock_translator_service):
    assert adapter_with_mock._translator_service == mock_translator_service()


async def handler_translator_async_handler_test(adapter, update, context, message):
    @adapter.handler_translator(message)
    async def test_func(update, context, message):
        assert message == "Hello World"

    result = await test_func(update, context, message)
    assert result is None


# async def handler_translator_sync_handler_test(adapter, update, context, message):
#     @adapter.handler_translator(message)
#     def test_func(update, context, message):
#         assert message == "Hello World"

#     result = test_func(update, context, message)
#     assert result is None


async def handler_translator_translation_async_handler_test(adapter, update, context):
    message = "Hello World"
    t_s_mock = adapter._translator_service
    w = await t_s_mock.translate_str(message, "fr")

    @adapter.handler_translator(message)
    async def func_test(update, context, message):
        assert w == "Bonjour le monde"

    result = await func_test(update, context, message)
    assert result is None


# async def handler_translator_translation_sync_handler_test(adapter, update, context):
#     message = "Hello World"
#     t_s_mock = adapter._translator_service
#     w = await t_s_mock.translate_str(message, "fr")

#     @adapter.handler_translator(message)
#     def func_test(update, context, message):
#         assert w == "Bonjour le monde"

#     result = func_test(update, context, message)
#     assert result is None


async def dynamic_handler_translator_with_async_handler_sync_function_test(
    adapter, update, context, message, translate_function
):
    context.args = "Hello World"

    @adapter.dynamic_handler_translator(translate_function, "en")
    async def test_func(update, context, message) -> None:
        assert message == "Greater than 10"


async def dynamic_handler_translator_with_async_handler_async_function_test(
    adapter, update, context, message, async_translate_function
):
    context.args = "Hello World"

    @adapter.dynamic_handler_translator(async_translate_function, "en")
    async def test_func(update, context, message) -> None:
        assert message == "Greater than 10"


async def dynamic_handler_translator_with_sync_handler_sync_function_test(
    adapter, update, context, message, translate_function
):
    context.args = "Hello World"

    @adapter.dynamic_handler_translator(translate_function, "en")
    def test_func(update, context, message) -> None:
        assert message == "Greater than 10"


async def dynamic_handler_translator_with_sync_handler_async_function_test(
    adapter, update, context, message, async_translate_function
):
    context.args = "Hello World"

    @adapter.dynamic_handler_translator(async_translate_function, "en")
    def test_func(update, context, message) -> None:
        assert message == "Greater than 10"

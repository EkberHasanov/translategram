def init_test(adapter_with_mock, mock_translator_service):
    assert adapter_with_mock._translator_service == mock_translator_service()


async def handler_translator_test(adapter, update, context, message):
    async def test_func(update, context, message):
        assert message == "Hello World"
    wrapped_func = adapter.handler_translator(test_func, message)
    result = await wrapped_func(update, context, message)
    assert result is None


async def handler_translator_translation_test(adapter, update, context):
    message = 'Hello World'
    t_s_mock = adapter._translator_service
    w = await t_s_mock.translate_str(message, 'fr')

    async def func_test(update, context, message):
        assert w == "Bonjour le monde"

    wrapped_func = adapter.handler_translator(func_test, message)
    result = await wrapped_func(update, context, message)
    assert result is None

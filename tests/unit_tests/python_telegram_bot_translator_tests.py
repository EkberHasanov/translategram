def init_test(adapter_with_mock, mock_translator_service):
    assert adapter_with_mock._translator_service == mock_translator_service()


async def handler_translator_test(adapter, update, context, message):
    @adapter.handler_translator(message)
    async def test_func(update, context, message):
        assert message == "Hello World"

    result = await test_func(update, context, message)
    assert result is None


async def handler_translator_translation_test(adapter, update, context):
    message = 'Hello World'
    t_s_mock = adapter._translator_service
    w = await t_s_mock.translate_str(message, 'fr')

    @adapter.handler_translator(message)
    async def func_test(update, context, message):
        assert w == "Bonjour le monde"

    result = await func_test(update, context, message)
    assert result is None

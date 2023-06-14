import os
from pathlib import Path
from translategram.translategram.cache import Cache


def cache_initialization_with_default_name_test(cache: Cache, tmp_path: Path) -> None:
    assert cache._obj is not None
    assert str(cache.pickle_file) == str(tmp_path / "translation.data")


async def store_and_retrieve_large_data_test(cache: Cache) -> None:
    key = "key"
    value = "x" * 10_000_000  # Value of 10 MB

    await cache.store(key, value)
    retrieved_value = await cache.retrieve(key)

    assert retrieved_value == value


async def cache_file_handling_test(cache: Cache, tmp_path: Path) -> None:
    cache_file = tmp_path / "translation.data"
    assert cache_file.exists()

    key = "key"
    value = "value"
    await cache.store(key, value)

    assert os.path.getsize(str(cache_file)) > 0


#    del cache
#    assert not cache_file.exists()


async def store_and_retrieve_test(cache: Cache) -> None:
    await cache.store("key1", "value1")
    result = await cache.retrieve("key1")
    assert result == "value1"


async def retrieve_nonexistent_key_test(cache: Cache) -> None:
    result = await cache.retrieve("nonexistent_key")
    assert result is None


async def store_and_retrieve_multiple_values_test(cache: Cache) -> None:
    await cache.store("key1", "value1")
    await cache.store("key2", "value2")
    await cache.store("key3", "value3")

    result1 = await cache.retrieve("key1")
    result2 = await cache.retrieve("key2")
    result3 = await cache.retrieve("key3")

    assert result1 == "value1"
    assert result2 == "value2"
    assert result3 == "value3"

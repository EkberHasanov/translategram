import os
import pickle
from typing import Protocol, Union


class Cache(Protocol):
    """
    Protocol for defining a cache system.

    Implementing classes should provide functionality to store and retrieve values from the cache.
    """

    async def store(self, key: str, value: str) -> None:
        """
        Store the value in the cache associated with the specified key.

        :param key: The key to associate the value with.
        :param value: The value to store in the cache.
        """
        ...

    async def retrieve(self, key: str) -> Union[str, None]:
        """
        Retrieve the value from the cache associated with the specified key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key does not exist in the cache.
        """
        ...


class PickleCache:
    """
    Cache implementation using pickle serialization.

    This cache stores data in a pickle file on disk.
    """

    def __init__(self, obj: object, filename: str = "translation.data") -> None:
        """
        Initialize the PickleCache.

        :param obj: The object to be cached.
        :param filename: The name of the pickle file to store the cache data. Default is "translation.data".
        """
        self._obj = obj
        self.pickle_file = filename
        with open(self.pickle_file, "ab") as file:
            pickle.dump(self._obj, file)

    async def store(self, key: str, value: str) -> None:
        """
        Store the value in the cache associated with the specified key.

        :param key: The key to associate the value with.
        :param value: The value to store in the cache.
        """
        setattr(self._obj, key, value)
        with open(self.pickle_file, "wb") as file:
            pickle.dump(self._obj, file)

    async def retrieve(self, key: str) -> Union[str, None]:
        """
        Retrieve the value from the cache associated with the specified key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key does not exist in the cache.
        """
        with open(self.pickle_file, "rb") as file:
            loaded_data = pickle.load(file)
        return (
            loaded_data.__dict__.get(key)
            if isinstance(loaded_data.__dict__.get(key), str)
            else None
        )

    def __del__(self) -> None:
        """
        Clean up the cache file when the cache object is destroyed.
        """
        if os.path.exists(self.pickle_file):
            os.remove(self.pickle_file)

import pickle
from typing import Protocol, TypeVar, Union

T = TypeVar('T')


class Cache(Protocol):

    async def store(self, key: str, value: str) -> None:
        ...

    async def retrieve(self, key: str) -> Union[str, None]:
        ...


class PickleCache:
    def __init__(self, obj: T, filename: str = "translation.data") -> None:
        self._obj = obj
        self.pickle_file = filename
        with open(self.pickle_file, 'ab') as file:
            pickle.dump(self._obj, file)

    async def store(self, key: str, value: str) -> None:
        setattr(self._obj, key, value)
        with open(self.pickle_file, 'wb') as file:
            pickle.dump(self._obj, file)

    async def retrieve(self, key: str) -> Union[str, None]:
        with open(self.pickle_file, 'rb') as file:
            loaded_data = pickle.load(file)
        return loaded_data.__dict__.get(key) if isinstance(loaded_data.__dict__.get(key), str) else None

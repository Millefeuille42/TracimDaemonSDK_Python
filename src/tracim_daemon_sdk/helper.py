from json import loads, dumps
from typing import Any

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace


def decode_json(data: bytes) -> Any:
    return loads(data, object_hook=lambda d: Namespace(**d))


def encode_json(self) -> str:
    return dumps(self, default=lambda o: o.__dict__)

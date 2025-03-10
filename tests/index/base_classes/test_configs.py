from dataclasses import dataclass, field
from typing import Any, Dict, Type

import pytest
from pydantic import Field

from docarray import BaseDoc
from docarray.index.abstract import BaseDocIndex
from docarray.typing import NdArray

pytestmark = pytest.mark.index


class SimpleDoc(BaseDoc):
    tens: NdArray[10] = Field(dim=1000)


class FakeQueryBuilder:
    ...


@dataclass
class DBConfig(BaseDocIndex.DBConfig):
    work_dir: str = '.'
    other: int = 5


@dataclass
class RuntimeConfig(BaseDocIndex.RuntimeConfig):
    default_column_config: Dict[Type, Dict[str, Any]] = field(
        default_factory=lambda: {
            str: {
                'dim': 128,
                'space': 'l2',
            },
        }
    )
    default_ef: int = 50


def _identity(*x, **y):
    return x, y


class DummyDocIndex(BaseDocIndex):
    DBConfig = DBConfig
    RuntimeConfig = RuntimeConfig

    def python_type_to_db_type(self, x):
        return str

    _index = _identity
    num_docs = _identity
    _del_items = _identity
    _get_items = _identity
    execute_query = _identity
    _find = _identity
    _find_batched = _identity
    _filter = _identity
    _filter_batched = _identity
    _text_search = _identity
    _text_search_batched = _identity


def test_defaults():
    index = DummyDocIndex[SimpleDoc]()
    assert index._db_config.other == 5
    assert index._db_config.work_dir == '.'
    assert index._runtime_config.default_column_config[str] == {
        'dim': 128,
        'space': 'l2',
    }


def test_set_by_class():
    # change all settings
    index = DummyDocIndex[SimpleDoc](DBConfig(work_dir='hi', other=10))
    assert index._db_config.other == 10
    assert index._db_config.work_dir == 'hi'
    index.configure(RuntimeConfig(default_column_config={}, default_ef=10))
    assert index._runtime_config.default_column_config == {}

    # change only some settings
    index = DummyDocIndex[SimpleDoc](DBConfig(work_dir='hi'))
    assert index._db_config.other == 5
    assert index._db_config.work_dir == 'hi'
    index.configure(RuntimeConfig(default_column_config={}))
    assert index._runtime_config.default_column_config == {}


def test_set_by_kwargs():
    # change all settings
    index = DummyDocIndex[SimpleDoc](work_dir='hi', other=10)
    assert index._db_config.other == 10
    assert index._db_config.work_dir == 'hi'
    index.configure(default_column_config={}, default_ef=10)
    assert index._runtime_config.default_column_config == {}

    # change only some settings
    index = DummyDocIndex[SimpleDoc](work_dir='hi')
    assert index._db_config.other == 5
    assert index._db_config.work_dir == 'hi'
    index.configure(default_column_config={})
    assert index._runtime_config.default_column_config == {}


def test_default_column_config():
    index = DummyDocIndex[SimpleDoc]()
    assert index._runtime_config.default_column_config == {
        str: {
            'dim': 128,
            'space': 'l2',
        },
    }

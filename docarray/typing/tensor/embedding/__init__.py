from typing_extensions import TYPE_CHECKING

from docarray.typing.tensor.embedding.embedding import AnyEmbedding
from docarray.typing.tensor.embedding.ndarray import NdArrayEmbedding

__all__ = ['NdArrayEmbedding', 'AnyEmbedding']

from docarray.utils._internal.misc import import_library

if TYPE_CHECKING:
    from docarray.typing.tensor.embedding.tensorflow import TensorFlowEmbedding  # noqa
    from docarray.typing.tensor.embedding.torch import TorchEmbedding  # noqa


def __getattr__(name: str):
    if name == 'TorchEmbedding':
        import_library('torch', raise_error=True)
        from docarray.typing.tensor.embedding.torch import TorchEmbedding  # noqa

        __all__.append('TorchEmbedding')
        return TorchEmbedding

    elif name == 'TensorFlowEmbedding':
        import_library('tensorflow', raise_error=True)

        from docarray.typing.tensor.embedding.tensorflow import (  # noqa
            TensorFlowEmbedding,
        )

        __all__.append('TensorFlowEmbedding')
        return TensorFlowEmbedding

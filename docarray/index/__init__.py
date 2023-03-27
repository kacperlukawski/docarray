from docarray.utils.misc import import_library

__all__ = []


def __getattr__(name: str):
    if name == 'HnswDocumentIndex':
        import_library('hnswlib', raise_error=True)
        from docarray.index.backends.hnswlib import HnswDocumentIndex  # noqa: F401

        __all__.extend(['HnswDocumentIndex'])

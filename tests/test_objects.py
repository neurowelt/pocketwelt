import os

from pocketwelt import save_pickle, load_pickle


def test_pickle_ops() -> None:
    """
    Test saving and loading pickle objects.
    """
    obj = {
        "string": "Hello, World!",
        "integer": 42,
        "float": 3.14159,
        "boolean": True,
        "list": [1, 2, 3, 4, 5],
        "tuple": ("a", "b", "c"),
        "set": {1, 2, 3},
        "dictionary": {"key1": "value1", "key2": "value2"},
        "none": None,
        "bytes": b"binary data"
    }

    # Saving a pickle
    pickle_path = "tests/object.pkl"
    save_pickle(obj, path=pickle_path)

    # Loading a pickle
    loaded_obj = load_pickle(pickle_path)
    os.remove(pickle_path)

    assert loaded_obj == obj

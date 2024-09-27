from types import SimpleNamespace
from typing import Any, Dict, get_origin


class BaseConfig(SimpleNamespace):
    """
    Simple configuration class designed to work as pydantic BaseModel.

    Example:
        .. code-block:: python

            class ExampleConfig(BaseConfig):
                host: str
                port: int
                use_ssl: bool = False

            # Example usage
            example_config = ExampleConfig(host="localhost", port=8080)
            print(example_config.host)  # Output: localhost
            print(example_config.port)  # Output: 8080
            print(example_config.use_ssl)  # Output: False
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the BaseConfig instance.

        Args:
            **kwargs: Arbitrary keyword arguments representing configuration variables.

        Raises:
            AttributeError: If a provided keyword argument does not match any attribute in the class.
            TypeError: If a provided keyword argument does not match the expected type.
            ValueError: If any required arguments are missing.
        """
        # Very primitive way of disabling the direct construction
        assert (
            self.__class__.__base__ != SimpleNamespace
        ), "BaseConfig cannot be initiated directly - can only be used for class inheritance."

        # Construct the config
        _required = self._get_empty_attrs()
        for k, v in kwargs.items():
            # Check if attribute exists, retrieve type
            if not hasattr(self, k) and k not in self.__annotations__:
                raise AttributeError(
                    f"`{self.__class__.__name__}` does not contain config variable named `{k}`."
                )
            _type = self.__annotations__.get(k, None)

            # Check generic type origin to avoid TypeError
            if hasattr(_type, "__origin__"):
                _type = get_origin(_type)

            # Validate type & set attribute
            if _type and not isinstance(v, _type):
                raise TypeError(
                    f"`{k}` should be of type `{_type.__name__}`, but is of type`{type(v).__name__}`."
                )
            setattr(self, k, v)
            if k in _required:
                _required.remove(k)

        if len(_required) > 0:
            raise ValueError(
                f"The following arguments were missing: {','.join(_required)}"
            )

    def _get_empty_attrs(self):
        """
        Get a list of attributes that are annotated but not set.

        Returns:
            List[str]: A list of attribute names that are annotated but not set.
        """
        _empty_attrs = []
        for attr in self.__annotations__:
            if not hasattr(self, attr):
                _empty_attrs.append(attr)

        return _empty_attrs

    def to_dict(self) -> Dict[str, Any]:
        """
        Save the configuration to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the configuration.
        """
        _dict = {}
        for attr in self.__annotations__:
            _dict[attr] = getattr(self, attr, None)

        return _dict

    def to_txt(self, save_path: str) -> None:
        """
        Save the current config to a text file.

        Args:
            save_path (str): Path where the configuration text file will be saved.
        """
        with open(save_path, "w+") as f:
            for k, v in self.to_dict().items():
                f.write(f"{k}: {v}\n")

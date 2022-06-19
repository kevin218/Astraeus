from typing import Any
import xarray as xr


class Dataset(xr.Dataset):
	# Need to define this to avoid warning messages
    __slots__ = ("_dataset",)

    def __setattr__(self, name: str, value: Any) -> None:
        """Overwrite the setattr function to allow behaviour like
           Dataset.name = value instead of the usual
           Dataset['name'] = (coords, value).
        """
        try:
            object.__setattr__(self, name, value)
        except AttributeError as e:
            try:
                if str(e) != "{!r} object has no attribute {!r}".format(
                    type(self).__name__, name
                ):
                    raise e
                else:
                    self[name] = (list(self.coords), value)
            except Exception as e2:
                raise e2

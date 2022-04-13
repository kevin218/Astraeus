import pytest, os
import numpy as np
import xarray as xr
import astreus.xarrayIO as xrio

def test_writeH5():
    """
    Test writing Xarray dataset.
    """
    filename = "foo.h5"
    ds = xr.Dataset(
        {"foo": (("x", "y"), np.random.rand(4, 5))},
        coords={
            "x": [10, 20, 30, 40],
            "y": np.arange(5),
            "z": ("x", list("abcd")),
        },
    )
    success = xrio.writeXR(filename, ds)
    assert success == 1
    os.remove(filename)

def test_readH5():
    """
    Test reading Xarray dataset.
    """
    filename = "foo.h5"
    ds = xr.Dataset(
        {"foo": (("x", "y"), np.random.rand(4, 5))},
        coords={
            "x": [10, 20, 30, 40],
            "y": np.arange(5),
            "z": ("x", list("abcd")),
        },
    )
    success = xrio.writeXR(filename, ds)
    ds2, success = xrio.readXR(filename)
    assert success == 1
    assert np.array_equal(ds.foo.values, ds2.foo.values)
    os.remove(filename)

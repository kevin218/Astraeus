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
        {"foo": (("x", "y"), np.random.rand(4, 5)),
         "bar": (("x", "y"), np.random.rand(4, 5))},
        coords={
            "x": [10, 20, 30, 40],
            "y": np.arange(5),
            "z": ("x", list("abcd")),
        },
    )
    ds2 = xr.Dataset(
        {"foo2": (("x", "y"), np.random.rand(4, 5)),
         "bar2": (("x", "y"), np.random.rand(4, 5))},
        coords={
            "x": [10, 20, 30, 40],
            "y": np.arange(5),
            "z": ("x", list("abcd")),
        },
    )
    success = xrio.writeXR(filename, ds)
    assert success == 1
    success = xrio.writeXR(filename, ds2, append=True)
    assert success == 1
    os.remove(filename)

def test_readH5():
    """
    Test reading Xarray dataset.
    """
    filename = "foo.h5"
    ds = xr.Dataset(
        {"foo": (("x", "y"), np.random.rand(4, 5)),
         "bar": (("x", "y"), np.random.rand(4, 5))},
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

def test_makeDA():
    """
    Test making Xarray DataArrays.
    """
    flux = np.random.rand(10, 5, 20)
    time = np.arange(10)
    flux_unit = 'e-'
    time_unit = 'MJD'
    name = 'flux'
    flux_da = xrio.makeFluxLikeDA(flux, time, flux_unit, time_unit, name=name)
    assert np.array_equal(flux_da.values, flux)
    assert flux_da.name == name
    assert flux_da.attrs['time_unit'] == time_unit

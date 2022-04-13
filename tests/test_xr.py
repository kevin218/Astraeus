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
    # Create 3D DataArray of flux-like values (time, y, x)
    flux = np.random.rand(10, 5, 20)
    time = np.arange(10)
    flux_units = 'e-'
    time_units = 'MJD'
    name = 'flux'
    flux_da = xrio.makeFluxLikeDA(flux, time, flux_units, time_units, name=name)
    assert np.array_equal(flux_da.values, flux)
    assert flux_da.name == name
    assert flux_da.attrs['time_units'] == time_units
    # Create 1D DataArray of time-dependent values
    t = np.random.rand(10)
    t_units = 'K'
    name = 'Detector_Temperature'
    temp_da = xrio.makeTimeLikeDA(t, time, t_units, time_units, name=name)
    assert np.array_equal(temp_da.values, t)
    assert temp_da.name == name
    assert temp_da.attrs['units'] == t_units
    # Create 1D DataArray of wavelength-dependent values
    w = 1+np.random.rand(20)
    w_units = '%'
    name = 'Transit Depth'
    wavelength = np.linspace(1,5,20)
    wave_units = 'microns'
    wave_da = xrio.makeWaveLikeDA(w, wavelength, w_units, wave_units, name=name)
    assert np.array_equal(wave_da.values, w)
    assert wave_da.name == name
    assert wave_da.attrs['units'] == w_units

import pytest, os
import numpy as np
import xarray as xr
import astraeus.xarrayIO as xrio

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
    success = xrio.writeXR(filename, None)
    assert success == 0
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
    ds2 = xrio.readXR(filename)
    assert ds2 != None
    assert np.array_equal(ds.foo.values, ds2.foo.values)
    ds2  = xrio.readXR("bar.h5")
    assert ds2  == None
    os.remove(filename)

def test_makeDA():
    """
    Test making Xarray DataArrays and Datasets.
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
    name = 'detector_temperature'
    temp_da = xrio.makeTimeLikeDA(t, time, t_units, time_units, name=name)
    assert np.array_equal(temp_da.values, t)
    assert temp_da.name == name
    assert temp_da.attrs['units'] == t_units
    # Create 1D DataArray of wavelength-dependent values
    w = 1+np.random.rand(20)
    w_units = '%'
    name = 'transit_depth'
    wavelength = np.linspace(1,5,20)
    wave_units = 'microns'
    wave_da = xrio.makeWaveLikeDA(w, wavelength, w_units, wave_units, name=name)
    assert np.array_equal(wave_da.values, w)
    assert wave_da.name == name
    assert wave_da.attrs['units'] == w_units
    #Create 2D DataArray of wavelength- and time-dependent values
    name = 'light_curves'
    spec = np.sum(flux, axis=1).T
    lc_da = xrio.makeLCDA(spec, wavelength, time, flux_units, wave_units, time_units, name=name)
    assert np.array_equal(lc_da.values, spec)
    assert lc_da.name == name
    assert lc_da.wavelength.attrs['wave_units'] == wave_units
    # Create Xarray Dataset from multiple DataArrays
    dictionary = dict(flux=flux_da,t=temp_da,w=wave_da)
    ds1 = xrio.makeDataset(dictionary)
    assert np.array_equal(ds1.flux.values, flux_da.values)
    assert np.array_equal(ds1.t.values, temp_da.values)
    assert np.array_equal(ds1.w.values, wave_da.values)
    # Concatenate Xarray Datasets along time axis
    ds2 = xrio.makeDataset(dictionary)
    datasets = [ds1, ds2]
    ds = xrio.concat(datasets, dim='time')
    assert np.array_equal(ds.flux.values, np.concatenate((ds1.flux.values,ds2.flux.values)))

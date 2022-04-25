import numpy as np
import xarray as xr


def writeXR(filename, ds, verbose=True, append=False):
    """
    Save Xarray Dataset to an HDF5 file.

    Parameters
    ----------
    filename: str
        File name to save data, with our without extension
    ds: object
        Xarray Dataset to be saved
    verbose: boolean
        Set True to enable print statements declaring success/failure,
        and optional error message
    append: boolean
        Set True to add parameters to existing dataset.
        Concatenation of existing parameters is not supported.

    Returns
    -------
    success: boolean
        Return True is file was saved successfully
    """
    try:
        # Add .h5 if missing
        if (filename.endswith(".hdf5") == False) and \
           (filename.endswith(".h5") == False) and \
           (filename.endswith(".nc") == False):
            filename += ".h5"

        if append:
            ds.to_netcdf(filename, engine='h5netcdf', mode='a')
        else:
            ds.to_netcdf(filename, engine='h5netcdf')

        if verbose:
            print(f"Finished writing to {filename}")
        success = True
    except Exception as e:
        if verbose:
            print(f"Failed to write to {filename}")
            print(e)
        success = False
    return success


def readXR(filename, verbose=True):
    """
    Load Xarray Dataset from an HDF5 file.

    Parameters
    ----------
    filename: str
        File name to load data from, with our without extension

    Returns
    -------
    ds: object
        Xarray Dataset containing saved information.
    """
    try:
        # Add .h5 if missing
        if (filename.endswith(".hdf5") == False) and \
           (filename.endswith(".h5") == False) and \
           (filename.endswith(".nc") == False):
            filename += ".h5"
        ds = xr.open_dataset(filename, engine='h5netcdf')
        if verbose:
            print(f"Finished loading parameters from {filename}")
    except Exception as e:
        if verbose:
            print(f"Failed to load parameters from {filename}")
            print(e)
        ds = None
    return ds


def makeFluxLikeDA(flux, time, flux_units, time_units, name=None, y=None, x=None):
    """
    Make Xarray DataArray with flux-like dimensions (time, y, x).

    Parameters
    ----------
    flux: array
        3D array of flux or uncertainty values
    time: array
        1D array of time values
    flux_units: str
        Flux units (e.g., 'electrons')
    time_units: str
        Time units (e.g., 'BJD_TDB')
    name: str
        Name of flux-like array (e.g., 'flux_unc')
    y: array
        (Optional) 1D array of pixel positions, default is 0..flux.shape[1]
    x: array
        (Optional) 1D array of pixel positions, default is 0..flux.shape[2]

    Returns
    -------
    da: object
        Xarray DataArray
    """
    if y == None:
        y = np.arange(flux.shape[1])
    if x == None:
        x = np.arange(flux.shape[2])
    da = xr.DataArray(
        flux,
        name=name,
        coords={
            "time": time,
            "y": y,
            "x": x,
            },
        dims=["time", "y", "x", ],
        attrs={
            "flux_units": flux_units,
            "time_units": time_units,
            },
        )
    da["time"].attrs["time_units"] = time_units
    return da

def makeTimeLikeDA(t, time, units, time_units, name=None):
    """
    Make Xarray DataArray with time-like dimensions.

    Parameters
    ----------
    t: array
        1D array of time-dependent values
    time: array
        1D array of time values
    units: str
        units of t (e.g., 'K')
    time_units: str
        Time units (e.g., 'BJD_TDB')
    name: str
        Name of time-like array (e.g., 'detector_temperature')

    Returns
    -------
    da: object
        Xarray DataArray
    """
    da = xr.DataArray(
        t,
        name=name,
        coords={
            "time": time,
            },
        dims=["time"],
        attrs={
            "units": units,
            "time_units": time_units,
            },
        )
    da["time"].attrs["time_units"] = time_units
    return da

def makeWaveLikeDA(w, wavelength, units, wave_units, name=None):
    """
    Make Xarray DataArray with wavelength-like dimensions.

    Parameters
    ----------
    w: array
        1D array of wavelength-dependent values
    wavelength: array
        1D array of wavelength values
    units: str
        units of w (e.g., '%')
    wave_units: str
        Wavelength units (e.g., 'microns')
    name: str
        Name of wavelength-like array (e.g., 'Transit Depth')

    Returns
    -------
    da: object
        Xarray DataArray
    """
    da = xr.DataArray(
        w,
        name=name,
        coords={
            "wavelength": wavelength,
            },
        dims=["wavelength"],
        attrs={
            "units": units,
            "wave_units": wave_units,
            },
        )
    da["wavelength"].attrs["wave_units"] = wave_units
    return da

def makeLCDA(spec, wave, time, flux_units, wave_units, time_units, name=None):
    """
    Make Xarray DataArray with light curve (wavelength, time) dimensions.

    Parameters
    ----------
    spec: ndarray
        2D array of spectra or uncertainty values
    wave: ndarray
        1D array of wavelength values
    time: ndarray
        1D array of time values
    flux_units: str
        Flux units (e.g., 'electrons')
    wave_units: str
        Wavelength units (e.g., 'microns')
    time_units: str
        Time units (e.g., 'BJD_TDB')
    name: str
        Name of spec-like array (e.g., 'spec_unc')

    Returns
    -------
    da: object
        Xarray DataArray
    """
    da = xr.DataArray(
        spec,
        name=name,
        coords={
            "wavelength": wave,
            "time": time,
            },
        dims=["wavelength", "time", ],
        attrs={
            "flux_units": flux_units,
            "wave_units": wave_units,
            "time_units": time_units,
            },
        )
    da["wavelength"].attrs["wave_units"] = wave_units
    da["time"].attrs["time_units"] = time_units
    return da

def makeDataset(dictionary=None):
    """
    Make Xarray Dataset using dictionary of DataArrays.

    Parameters
    ----------
    dictionary: dict
        Dictionary of DataArrays (e.g., dict(flux=flux_da,t=temp_da,w=wave_da))

    Returns
    -------
    ds: object
        Xarray Dataset
    """
    ds = xr.Dataset(dictionary)
    return ds

def concat(datasets, dim='time', data_vars='minimal', coords='minimal', compat='override'):
    """
    Concatenate list of Xarray Datasets along given dimension.  See xarray.concat() for details.

    Parameters
    ----------
    datasets: list
        List of Xarray Dataset objects
    dim: str
        Name of the dimension to concatenate along
    data_vars: str
        {"minimal", "different", "all"}
    coords: str
        {"minimal", "different", "all"}
    compat: str
        {"identical", "equals", "broadcast_equals", "no_conflicts", "override"}

    Returns
    -------
    ds: object
        Xarray Dataset with concatenated parameters
    """
    ds = xr.concat(datasets, dim=dim, data_vars=data_vars, coords=coords, compat=compat)
    return ds

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

    Returns
    -------
    success: boolean
        Return True is file was saved successfully
    """
    try:
        # Add .hdf5 if missing
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
    success: boolean
        Return True is file was loaded successfully
    """
    try:
        # Add .hdf5 if missing
        if (filename.endswith(".hdf5") == False) and \
           (filename.endswith(".h5") == False) and \
           (filename.endswith(".nc") == False):
            filename += ".h5"

        ds = xr.open_dataset(filename, engine='h5netcdf')

        if verbose:
            print(f"Finished loading parameters from {filename}")
        success = True
    except Exception as e:
        if verbose:
            print(f"Failed to load parameters from {filename}")
            print(e)
        success = False
        ds = None
    return ds, success


def makeFluxLikeDA(flux, time, flux_unit, time_unit, name=None, y=None, x=None):
    """
    Make Xarray DataArray with flux-like dimensions (time, y, x).

    Parameters
    ----------
    flux: array
        3D array of flux or uncertainty values
    time: array
        1D array of time values
    flux_unit: str
        Flux units (e.g., 'electrons')
    time_unit: str
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
            "flux_unit": flux_unit,
            "time_unit": time_unit,
            },
        )
    return da


def makeDataset():
    """
    Make Xarray Dataset using list of DataArrays.

    Parameters
    ----------
    filename: str
        ...

    Returns
    -------
    ds: object
        Xarray Dataset
    """

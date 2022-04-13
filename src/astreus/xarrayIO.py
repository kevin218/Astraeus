import numpy as np
import xarray as xr


def writeXR(filename, ds, verbose=True):
    """
    Save Xarray dataset to an HDF5 file.

    Parameters
    ----------
    filename: str
        File name to save data, with our without extension
    ds: object
        Xarray dataset to be saved
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
    Load Xarray dataset from an HDF5 file.

    Parameters
    ----------
    filename: str
        File name to load data from, with our without extension

    Returns
    -------
    ds: object
        Xarray dataset containing saved information.
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

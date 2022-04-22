import h5py

# Empty Data object
class Data():
    """
    Data object containing parameters loaded from HDF5 file.
    """
    def __init(self):
        return

def writeH5(filename, verbose=True, **kwargs):
    """
    Save keyword arguments to an HDF5 file.

    Parameters
    ----------
    filename: str
        File name to save data, with our without extension
    verbose: boolean
        Set True to enable print statements declaring success/failure,
        and optional error message
    **kwargs: number, array
        Parameters to save

    Returns
    -------
    success: boolean
        Return True is file was saved successfully
    """
    try:
        # Add .hdf5 if missing
        if (filename.endswith(".hdf5") == False) and (filename.endswith(".h5") == False):
            filename += ".h5"
        # Open File object for writing
        # f = h5py.File(filename, "w")
        with h5py.File(filename, "w") as f:
            for key, value in kwargs.items():
                dset = f.create_dataset(key, data=value, compression="gzip")
        if verbose:
            print(f"Finished writing to {filename}")
        success = True
    except Exception as e:
        if verbose:
            print(f"Failed to write to {filename}")
            print(e)
        success = False
    return success


def readH5(filename, verbose=True, data=None, keys=None):
    """
    Load parameters from an HDF5 file to an object.

    Parameters
    ----------
    filename: str
        File name to load data from, with our without extension
    verbose: boolean
        Set True to enable print statements declaring success/failure,
        and optional error message
    data: object
        Data object instance that parameters are added to.
        If None, then data object will be created.
    keys: list
        List of keyword parameters to read from file.
        If None, then all keywords will be read in.

    Returns
    -------
    data: object
        Data object instance that parameters are added to.
    success: boolean
        Return True is file was loaded successfully
    """
    try:
        # Add .hdf5, if missing
        if (filename.endswith(".hdf5") == False) and (filename.endswith(".h5") == False):
            filename += ".h5"
        # Creat instance, if None
        if data == None:
            data = Data()
        # Open File object to read
        with h5py.File(filename, "r") as f:
            if keys == None:
                keys = []
                f.visit(keys.append)
            for key in keys:
                exec('data.'+key+' = f["'+key+'"][()]')
        if verbose:
            print(f"Finished loading parameters from {filename}")
        success = True
    except Exception as e:
        if verbose:
            print(f"Failed to load parameters from {filename}")
            print(e)
        success = False
    return data, success

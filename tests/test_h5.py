import pytest, os
import numpy as np
import astraeus.hdf5IO as h5io

def test_writeH5():
    """
    Test writing HDF5 file.
    """
    flux = np.ones((5,5))
    time = np.arange(5)
    filename = "foo.hdf5"
    success = h5io.writeH5(filename, flux=flux, time=time)
    assert success == 1
    success = h5io.writeH5(filename, flux=flux, time=time, verbose=False)
    assert success == 1
    os.remove(filename)

def test_readH5():
    """
    Test reading HDF5 file.
    """
    flux = np.ones((5,5))
    time = np.arange(5)
    filename = "foo.hdf5"
    success = h5io.writeH5(filename, flux=flux, time=time)
    data, success = h5io.readH5(filename)
    assert success == 1
    assert np.array_equal(data.time, time)
    data, success = h5io.readH5(filename, keys=['flux'])
    assert success == 1
    assert np.array_equal(data.flux, flux)
    data, success = h5io.readH5(filename, verbose=False)
    assert success == 1
    data, success = h5io.readH5("bar.hdf5", verbose=False)
    assert success == 0
    os.remove(filename)

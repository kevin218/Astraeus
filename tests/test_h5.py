import pytest, os
import numpy as np
import astraeus.hdf5IO as h5io

"""
pytest --cov=.
"""

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
    data = h5io.readH5(filename)
    assert np.array_equal(data.time, time)
    data = h5io.readH5(filename, keys=['flux'])
    assert np.array_equal(data.flux, flux)
    data = h5io.readH5(filename, verbose=False)
    assert data != None
    data = h5io.readH5("bar.hdf5", verbose=False)
    assert data == None
    os.remove(filename)

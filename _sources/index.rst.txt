.. Astraeus documentation master file, created by
   sphinx-quickstart on Tue Mar 22 13:13:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for Astraeus
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

`Astraeus` is a general-purpose tool that manages your data using Xarray structures and reads/writes data from/to your exoplanet data reduction pipeline.  By using consistent formats and keywords across pipelines, users will be able to exchange and compare results easier than ever before!  `Astraeus` makes use of `Xarray`, an open source Python package that uses labelled multi-dimensional arrays (think of Pandas in N dimensions).

`Xarray` is commonly used for data analysis in geoscience and makes use of two core data structures, called a `DataArray` and a `Dataset`.  The former is like a NumPy array, except with coordinates, labels, and attributes.  The latter is simply a collection of DataArrays.  Both structures can easily be written to and loaded from HDF5 files.  This means, even if you are not using Python, you can still read an HDF5 file written by `Astraeus` and maintain the full useability of your data.


Indices and Searching
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Installation
============

The fastest way to install `Astraeus` is to use ``pip``::

    pip install git+https://github.com/kevin218/Astraeus.git

If you plan on contributing to the package, you should instead clone it via GitHub::

    git clone https://github.com/kevin218/Astraeus.git
    cd Astraeus
    pip install -e .

The ``-e`` flag makes the install editable, which means that you do not have to install the package again and again after each change.  Changes to your files inside the project folder will automatically reflect in changes on your installed package.  However, if you are working in an interactive environment (e.g., ipython, Jupyter) you will need to re-import any modules that have changed.


Example Usage
=============

`Astraeus` has several templates for creating Xarray DataArrays: `flux-like`, `time-like`, `wavelength-like`, and `light curve` (which makes use of both time and wavelength).

Creating an `flux-like` DataArray requires a 3D array (time, y, x) of flux-like values, a time array, and (of course) units::

    # Create 3D DataArray of flux-like values (time, y, x)
    import astraeus.xarrayIO as xrio
    flux = np.random.rand(10, 5, 20)
    time = np.arange(10)
    flux_units = 'e-'
    time_units = 'MJD'
    name = 'flux'
    flux_da = xrio.makeFluxLikeDA(flux, time, flux_units, time_units,
                                  name=name)

The `time-like` and `wavelength-like` DataArrays are quite similar, and are helpful for recording time- and wavelength-dependent variables::

    # Create 1D DataArray of time-dependent values
    temperature = np.random.rand(10)
    time = np.arange(10)
    units = 'K'
    time_units = 'MJD'
    name = 'detector_temperature'
    temp_da = xrio.makeTimeLikeDA(temperature, time, units,
                                  time_units, name=name)

    # Create 1D DataArray of wavelength-dependent values
    depth = 1+np.random.rand(20)
    wavelength = np.linspace(1,5,20)
    units = '%'
    wave_units = 'microns'
    name = 'transit_depth'
    depth_da = xrio.makeWaveLikeDA(depth, wavelength, units,
                                   wave_units, name=name)

A `light curve` DataArray is used to store, for example, a time series of 1D spectra and requires a 2D array (wavelength, time) of flux-like values, a time array, and (of course) units::

    #Create 2D DataArray of wavelength- and time-dependent values
    spec = np.random.rand(20, 10)
    wavelength = np.linspace(1,5,20)
    time = np.arange(10)
    flux_units = 'e-'
    wave_units = 'microns'
    time_units = 'MJD'
    name = 'light_curves'
    lc_da = xrio.makeLCDA(spec, wavelength, time, flux_units,
                          wave_units, time_units, name=name)

Maintaining all of these DataArrays can be cumbersome, so it is often helpful to combine DataArrays with similar coordinates (i.e., axes) into an Xarray Dataset::

    # Create Xarray Dataset from multiple DataArrays
    dictionary = dict(flux=flux_da,temp=temp_da,depth=depth_da)
    ds = xrio.makeDataset(dictionary)

People often analyze segments (or files) from a larger dataset before combining the results.  If need be, one can concatenate multiple Datasets along a given axis (often time)::

    # Concatenate two Xarray Datasets along time axis
    dictionary = dict(flux=flux_da,temp=temp_da,depth=depth_da)
    ds1 = xrio.makeDataset(dictionary)
    ds2 = xrio.makeDataset(dictionary)
    datasets = [ds1, ds2]
    ds = xrio.concat(datasets, dim='time')

Finally, writing and reading Xarray Datasets and DataArrays is straightforward::

    filename = "foo.h5"
    success = xrio.writeXR(filename, ds)

    ds = xrio.readXR(filename)

Alternatively, to read and write generic parameters directly to an HDF5 file, use the functions within  ``astraeus.hdf5IO``::

    import astraeus.hdf5IO as h5io
    flux = np.ones((5,5))
    time = np.arange(5)
    filename = "foo.hdf5"
    success = h5io.writeH5(filename, flux=flux, time=time)

    data = h5io.readH5(filename)

Results are returned in a `data` object and can be accessed using ``data.flux`` and ``data.time``.


Code
====

.. The following will add the signature of the individual functions and pull their docstrings.

.. automodapi:: astraeus.xarrayIO
.. automodapi:: astraeus.hdf5IO

..
    Recipes
    -------

    To save generic outputs directly to an HDF5 file,
    you can use the ``astraeus.hdf5IO.writeH5()`` function:

    .. py:function:: astraeus.hdf5IO.writeH5(filename, verbose=True, **kwargs)

       Save keyword arguments to a generic HDF5 file.

       :param filename: File name to save data, with our without extension
       :type filename: str
       :param verbose: Set True to enable print statements declaring success/failure, and optional error message
       :param **kwargs: Parameters to save
       :return: Return True is file was saved successfully
       :rtype: boolean


..
    More about how to describe code can be hound
    `here <https://www.sphinx-doc.org/en/master/tutorial/describing-code.html>`_

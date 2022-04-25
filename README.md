# Astraeus
A tool for standardizing I/O when reducing and analyzing exoplanet data

`Astraeus` is a general-purpose tool that manages your data using Xarray structures and reads/writes data from/to your exoplanet data reduction pipeline.  By using consistent formats and keywords across pipelines, users should be able to exchange and compare results easier than ever before!  `Astraeus` makes use of `Xarray`, an open source Python package that uses labelled multi-dimensional arrays (think of Pandas in N dimensions).

`Xarray` is commonly used for data analysis in geoscience and makes use of two core data structures, called a `DataArray` and a `Dataset`.  The former is like a NumPy array, except with coordinates, labels, and attributes.  The latter is simply a collection of DataArrays.  Both structures can easily be written to and loaded from HDF5 files.  This means, even if you are not using Python, you can still read an HDF5 file written by `Astraeus` and maintain the full useability of your data.


## Installation & Documentation

Up-to-date installation instructions and documentation can be found at
[https://kevin218.github.io/Astraeus/](https://kevin218.github.io/Astraeus/).

## Quickstart

Stay tuned for our quickstart guide.

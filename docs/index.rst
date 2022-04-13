.. Astreus documentation master file, created by
   sphinx-quickstart on Tue Mar 22 13:13:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for Astreus
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Astreus is a general-purpose tool that saves/loads data from/to your exoplanet data reduction pipeline.  By using consistent formats and keywords across pipelines, users should be able to exchange and compare results easier than ever before!


Usage
=====

.. _installation:

Installation
------------

To use `Astreus` you need to install TBD...


.. _code:

Code
----

To save outputs directly to an HDFs file, you can use the ``astreus.hdf5IO.writeH5()`` function:

.. py:function:: astreus.hdf5IO.writeH5(filename, verbose=True, **kwargs)

    :filename: File name to save data, with our without extension
    :verbose: Set True to enable print statements declaring success/failure, and optional error message
    :**kwargs: Parameters to save

    .. py:exception:: TypeError

   Raised if write is unsuccessful.

More about how to describe code can be hound
`here <https://www.sphinx-doc.org/en/master/tutorial/describing-code.html>`_


..
  The following section creates an index, a list of modules and a
  search page.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

..
 The following will add the signature of the individual functions and pull
 their docstrings.

.. automodapi:: astreus.hdf5IO
.. automodapi:: astreus.xarrayIO

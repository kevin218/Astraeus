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

To use `Astreus` you need to install X, Y and Z.


.. _code:

Code
----

Here is an example of describing the use of your function.

To add one to a number you can use the ``astreus.add_one()`` function:

.. py:function:: astreus.add_one(number)


    :param number: Should be integer, floating point number or a string.

    If ``number`` is not one of these types, an exception will be raised:

    .. py:exception:: TypeError

   Raised if the input is invalid.

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

.. automodapi:: astreus.example

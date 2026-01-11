asimov-bayeswave
================

BayesWave pipeline integration for Asimov.

``asimov-bayeswave`` is a plugin package that provides integration between
the `Asimov <https://git.ligo.org/asimov/asimov>`_ workflow management system
and the `BayesWave <https://git.ligo.org/lscsoft/bayeswave>`_ gravitational
wave parameter estimation pipeline.

Installation
------------

To install ``asimov-bayeswave``, use pip:

.. code-block:: bash

   pip install asimov-bayeswave

Or for development:

.. code-block:: bash

   git clone https://github.com/transientlunatic/asimov-bayeswave.git
   cd asimov-bayeswave
   pip install -e ".[docs,test]"

Usage
-----

Once installed, the BayesWave pipeline will be automatically available in Asimov
through the plugin system. You can use it in your production configuration files:

.. code-block:: yaml

   name: GW150914
   productions:
   - Prod0:
       pipeline: bayeswave
       comment: PSD generation
       status: wait

The plugin will be automatically discovered and loaded by Asimov through the
entry points system.

Features
--------

* Complete BayesWave pipeline integration for Asimov
* Automatic PSD generation and collection
* XML format PSD conversion
* HTCondor DAG generation and submission
* Post-processing and result collection
* PSD suppression capabilities
* Megaplot output collection and visualization

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   contributing

API Reference
-------------

.. autosummary::
   :toctree: _autosummary
   :recursive:

   asimov_bayeswave

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

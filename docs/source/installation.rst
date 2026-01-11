Installation
============

Requirements
------------

``asimov-bayeswave`` requires:

* Python >= 3.9
* asimov >= 0.7.0
* numpy

The BayesWave pipeline itself must be installed separately. See the
`BayesWave documentation <https://git.ligo.org/lscsoft/bayeswave>`_
for installation instructions.

Installing from PyPI
--------------------

The recommended way to install ``asimov-bayeswave`` is using pip:

.. code-block:: bash

   pip install asimov-bayeswave

Installing from Source
----------------------

To install from source for development:

.. code-block:: bash

   git clone https://github.com/transientlunatic/asimov-bayeswave.git
   cd asimov-bayeswave
   pip install -e ".[docs,test]"

This will install the package in editable mode with optional dependencies
for building documentation and running tests.

Verifying Installation
----------------------

To verify that the plugin is correctly installed and discovered by Asimov:

.. code-block:: python

   from asimov.pipelines import known_pipelines

   print("bayeswave" in known_pipelines)  # Should print: True

Or check from the command line:

.. code-block:: bash

   python -c "from asimov.pipelines import known_pipelines; print('bayeswave' in known_pipelines)"

Usage
=====

Basic Usage
-----------

Once ``asimov-bayeswave`` is installed, it will be automatically available
in Asimov. You can specify it as the pipeline in your production configuration:

.. code-block:: yaml

   name: GW150914
   productions:
   - Prod0:
       pipeline: bayeswave
       comment: PSD generation with BayesWave
       status: wait
       meta:
         likelihood:
           sample rate: 2048
           segment length: 8
         data:
           channels:
             H1: H1:GDS-CALIB_STRAIN
             L1: L1:GDS-CALIB_STRAIN
         quality:
           minimum frequency:
             H1: 20
             L1: 20

Configuration
-------------

BayesWave jobs are configured through the production metadata. Key configuration
sections include:

Likelihood Settings
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   likelihood:
     sample rate: 2048          # Sampling rate in Hz
     segment length: 8          # Segment length in seconds
     window length: 4           # Window length (optional)
     psd length: 8              # PSD estimation length
     roll off time: 1.0         # Roll-off time
     iterations: 100000         # Number of MCMC iterations
     chains: 8                  # Number of parallel chains
     threads: 4                 # Threads per chain

Data Settings
~~~~~~~~~~~~~

.. code-block:: yaml

   data:
     channels:
       H1: H1:GDS-CALIB_STRAIN
       L1: L1:GDS-CALIB_STRAIN
     frame types:
       H1: H1_HOFT_C00
       L1: L1_HOFT_C00
     cache files:               # Optional: use pre-generated cache files
       H1: /path/to/H1.cache
       L1: /path/to/L1.cache
     segment length: 8

Quality Settings
~~~~~~~~~~~~~~~~

.. code-block:: yaml

   quality:
     minimum frequency:
       H1: 20
       L1: 20
     lowest minimum frequency: 20  # Auto-calculated if not provided
     supress:                      # Optional: suppress frequency bands
       H1:
         lower: 60
         upper: 60.5

Scheduler Settings
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   scheduler:
     accounting group: ligo.dev.o4.cbc.pe.bayeswave
     request memory: 8192 MB
     request post memory: 16384 MB
     request disk: 64 MB
     request post disk: 64 MB
     copy frames: false          # Copy frame files to run directory
     osg: false                  # Use OSG resources

Working with PSDs
-----------------

BayesWave produces power spectral density (PSD) estimates that can be used
by downstream parameter estimation pipelines. The plugin automatically:

1. Collects PSDs from the BayesWave output
2. Converts them to XML format for use with LALInference
3. Stores them in the Asimov storage system
4. Commits them to the event repository

Accessing PSDs Programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from asimov_bayeswave import BayesWave

   # After job completion
   pipeline = BayesWave(production)
   assets = pipeline.collect_assets()

   # Access ASCII PSDs
   for ifo, psd_path in assets["psds"].items():
       print(f"{ifo}: {psd_path}")

   # Access XML PSDs
   for ifo, psd_path in assets["xml psds"].items():
       print(f"{ifo}: {psd_path}")

PSD Suppression
~~~~~~~~~~~~~~~

You can suppress specific frequency bands in the PSD (e.g., to remove
instrumental lines):

.. code-block:: python

   pipeline = BayesWave(production)
   pipeline.supress_psd(ifo="H1", fmin=60.0, fmax=60.5)

This sets the PSD to 1.0 in the specified frequency range.

Advanced Features
-----------------

Job Resurrection
~~~~~~~~~~~~~~~~

If a BayesWave job fails, it can be automatically resurrected using
HTCondor rescue DAGs:

.. code-block:: python

   pipeline = BayesWave(production)
   pipeline.resurrect()

This will resubmit the job using any available rescue files, up to
a maximum of 5 attempts.

HTML Output
~~~~~~~~~~~

The plugin automatically collects megaplot output for visualization:

.. code-block:: python

   pipeline = BayesWave(production)
   html_output = pipeline.html()

This generates HTML links to the megaplot results page.

Command Line Usage
------------------

If you're using Asimov's command-line interface:

.. code-block:: bash

   # Build the DAG
   asimov manage build --production Prod0

   # Submit the job
   asimov manage submit --production Prod0

   # Check status
   asimov manage monitor

The BayesWave plugin will be used automatically based on your
production configuration.

Contributing
============

Contributions to ``asimov-bayeswave`` are welcome! This page provides
guidelines for contributing to the project.

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork:

   .. code-block:: bash

      git clone https://github.com/YOUR_USERNAME/asimov-bayeswave.git
      cd asimov-bayeswave

3. Install in development mode with test dependencies:

   .. code-block:: bash

      pip install -e ".[docs,test]"

4. Create a new branch for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

Running Tests
-------------

The project uses pytest for testing. To run the test suite:

.. code-block:: bash

   pytest

To run with coverage reporting:

.. code-block:: bash

   pytest --cov=asimov_bayeswave --cov-report=html

Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in ``docs/build/html/``.

Code Style
----------

Please follow these guidelines:

* Use PEP 8 style for Python code
* Include docstrings for all public functions and classes
* Use NumPy-style docstrings
* Add type hints where appropriate
* Keep line length to 100 characters or less

Submitting Changes
------------------

1. Commit your changes with clear, descriptive commit messages
2. Push to your fork
3. Submit a pull request to the main repository
4. Ensure all CI checks pass

Your pull request should:

* Include tests for new functionality
* Update documentation as needed
* Pass all existing tests
* Follow the project's code style

Reporting Issues
----------------

If you find a bug or have a feature request, please open an issue on
the GitHub issue tracker. Include:

* A clear description of the issue
* Steps to reproduce (for bugs)
* Expected vs. actual behavior
* Your environment (OS, Python version, asimov version, etc.)

License
-------

By contributing to asimov-bayeswave, you agree that your contributions
will be licensed under the project's license.

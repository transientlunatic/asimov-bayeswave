# asimov-bayeswave

[![Tests](https://github.com/transientlunatic/asimov-bayeswave/actions/workflows/tests.yml/badge.svg)](https://github.com/transientlunatic/asimov-bayeswave/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/asimov-bayeswave/badge/?version=latest)](https://asimov-bayeswave.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/asimov-bayeswave.svg)](https://badge.fury.io/py/asimov-bayeswave)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

BayesWave pipeline integration for [Asimov](https://git.ligo.org/asimov/asimov).

This package provides a plugin for Asimov 0.7+ that enables integration with the BayesWave parameter estimation pipeline for gravitational wave data analysis.

## Features

- 🔌 **Plugin Architecture**: Seamlessly integrates with Asimov via entry points
- 📊 **PSD Generation**: Automatic power spectral density estimation and collection
- 🔄 **Format Conversion**: Converts PSDs to XML format for use with other pipelines
- 🚀 **HTCondor Integration**: Automated DAG generation and job submission
- 📈 **Result Collection**: Automatic collection of megaplot outputs and visualizations
- 🎯 **PSD Suppression**: Support for suppressing frequency bands in PSDs
- 🧪 **Well Tested**: Comprehensive unit test coverage

## Installation

### From PyPI (when released)

```bash
pip install asimov-bayeswave
```

### From Source

```bash
git clone https://github.com/transientlunatic/asimov-bayeswave.git
cd asimov-bayeswave
pip install -e .
```

### For Development

```bash
pip install -e ".[docs,test]"
```

## Quick Start

Once installed, the BayesWave pipeline is automatically available in Asimov. 
To add a new bayeswave analysis you can create a blueprint YAML file like the following:

```yaml
kind: analysis
pipeline: bayeswave
comment: PSD generation with BayesWave
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
```

## Usage

### Via Asimov CLI

```bash
# Build the DAG
asimov manage build --production Prod0

# Submit the job
asimov manage submit --production Prod0

# Monitor progress
asimov manage monitor
```

### Via Python API

```python
from asimov_bayeswave import BayesWave

# Create pipeline instance
pipeline = BayesWave(production)

# Build and submit
pipeline.build_dag()
pipeline.submit_dag()

# Collect results after completion
assets = pipeline.collect_assets()
psds = assets["psds"]
xml_psds = assets["xml psds"]
```

## Requirements

- Python >= 3.9
- asimov >= 0.7.0
- numpy
- BayesWave (must be installed separately)

## Documentation

Full documentation is available at [asimov-bayeswave.readthedocs.io](https://asimov-bayeswave.readthedocs.io).

### Building Documentation Locally

```bash
cd docs
make html
```

The built documentation will be in `docs/build/html/`.

## Testing

Run the test suite with:

```bash
pytest
```

For coverage reporting:

```bash
pytest --cov=asimov_bayeswave --cov-report=html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- New features include tests
- Documentation is updated
- Code follows PEP 8 style guidelines

## Migration from Asimov 0.6

If you're upgrading from Asimov 0.6 which included BayesWave support natively:

1. Install this plugin: `pip install asimov-bayeswave`
2. The plugin will be automatically discovered by Asimov 0.7+
3. No changes to your configuration files are required

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Daniel Williams (daniel.williams@ligo.org)

## Acknowledgments

- The LIGO Scientific Collaboration
- The BayesWave development team
- The Asimov development team

## Citation

If you use this software in your research, please cite:

```bibtex
@software{asimov_bayeswave,
  author = {Williams, Daniel},
  title = {asimov-bayeswave: BayesWave integration for Asimov},
  url = {https://github.com/transientlunatic/asimov-bayeswave},
  year = {2026}
}
```

## Support

For issues, questions, or contributions, please use the [GitHub issue tracker](https://github.com/transientlunatic/asimov-bayeswave/issues).

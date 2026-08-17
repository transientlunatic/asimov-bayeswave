"""BayesWave Pipeline integration for Asimov."""

from .bayeswave import BayesWave

__all__ = ["BayesWave"]

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

"""BayesWave Pipeline integration for Asimov."""

from .bayeswave import BayesWave

__all__ = ["BayesWave"]

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

"""Pytest configuration and fixtures."""

import os
import tempfile
from unittest.mock import MagicMock, Mock
import pytest


@pytest.fixture
def mock_production():
    """Create a mock production object for testing."""
    production = MagicMock()
    production.name = "TestProduction"
    production.pipeline = "bayeswave"
    production.category = "analyses"
    production.rundir = "/tmp/test_rundir"
    production.status = "wait"
    production.job_id = None

    # Mock event
    production.event = MagicMock()
    production.event.name = "GW150914"
    production.event.repository = MagicMock()
    production.event.repository.directory = "/tmp/test_repo"

    # Mock metadata
    production.meta = {
        "event time": 1126259462.4,
        "interferometers": ["H1", "L1"],
        "likelihood": {
            "sample rate": 2048,
            "segment length": 8,
            "segment start": -4,
        },
        "data": {
            "channels": {
                "H1": "H1:GDS-CALIB_STRAIN",
                "L1": "L1:GDS-CALIB_STRAIN",
            },
            "frame types": {
                "H1": "H1_HOFT_C00",
                "L1": "L1_HOFT_C00",
            },
            "cache files": {},
            "segment length": 8,
        },
        "quality": {
            "minimum frequency": {"H1": 20, "L1": 20},
        },
        "scheduler": {
            "accounting group": "ligo.dev.o4.cbc.pe.bayeswave",
        },
    }

    production.get_meta = lambda key: production.meta.get(key)

    return production


@pytest.fixture
def mock_config(monkeypatch):
    """Mock the asimov config object."""
    config_values = {
        ("general", "calibration_directory"): "analyses",
        ("general", "rundir_default"): "/tmp/run",
        ("general", "webroot"): "/tmp/web",
        ("pipelines", "environment"): "/opt/conda",
        ("logging", "directory"): "/tmp/logs",
        ("storage", "directory"): "/tmp/storage",
        ("condor", "user"): "test.user",
    }

    def mock_get(section, key):
        return config_values.get((section, key), "")

    # Create a mock module
    mock_config_module = MagicMock()
    mock_config_module.get = mock_get

    monkeypatch.setattr("asimov_bayeswave.bayeswave.config", mock_config_module)
    return mock_config_module


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

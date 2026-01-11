"""Tests for the BayesWave pipeline integration."""

import os
from unittest.mock import MagicMock, Mock, patch, mock_open
import pytest
import numpy as np

from asimov_bayeswave import BayesWave
from asimov.pipeline import PipelineException


class TestBayesWaveInit:
    """Test BayesWave initialization."""

    def test_init_success(self, mock_production, mock_config):
        """Test successful initialization."""
        pipeline = BayesWave(mock_production)
        assert pipeline.name == "BayesWave"
        assert pipeline.production == mock_production
        assert "wait" in pipeline.STATUS

    def test_init_wrong_pipeline(self, mock_production, mock_config):
        """Test initialization with wrong pipeline name."""
        mock_production.pipeline = "bilby"
        with pytest.raises(PipelineException, match="Pipeline mismatch"):
            BayesWave(mock_production)

    def test_init_sets_lowest_frequency(self, mock_production, mock_config):
        """Test that lowest minimum frequency is set."""
        pipeline = BayesWave(mock_production)
        assert "lowest minimum frequency" in mock_production.meta["quality"]
        assert mock_production.meta["quality"]["lowest minimum frequency"] == 20


class TestBayesWaveFlow:
    """Test the flow property."""

    def test_flow_calculation(self, mock_production, mock_config):
        """Test minimum frequency calculation."""
        mock_production.meta["quality"]["minimum frequency"] = {
            "H1": 20,
            "L1": 25,
            "V1": 15,
        }
        pipeline = BayesWave(mock_production)
        assert pipeline.flow == 15

    def test_flow_single_ifo(self, mock_production, mock_config):
        """Test flow with single interferometer."""
        mock_production.meta["quality"]["minimum frequency"] = {"H1": 30}
        pipeline = BayesWave(mock_production)
        assert pipeline.flow == 30


class TestBuildDag:
    """Test DAG building."""

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    @patch("asimov_bayeswave.bayeswave.open", new_callable=mock_open)
    def test_build_dag_success(
        self, mock_file, mock_popen, mock_production, mock_config
    ):
        """Test successful DAG building."""
        # Mock successful bayeswave_pipe execution
        mock_process = Mock()
        mock_process.communicate.return_value = (b"To submit: condor_submit", b"")
        mock_popen.return_value = mock_process

        # Mock get_configuration
        mock_ini = MagicMock()
        mock_ini._get_user = Mock(return_value="test.user")
        mock_ini.ini_loc = "/tmp/test.ini"
        mock_production.get_configuration.return_value = mock_ini

        pipeline = BayesWave(mock_production)
        pipeline.build_dag(user="test.user", dryrun=False)

        # Verify bayeswave_pipe was called
        assert mock_popen.called
        call_args = mock_popen.call_args[0][0]
        assert "bayeswave_pipe" in call_args[0]
        assert any("--trigger-time" in arg for arg in call_args)

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    def test_build_dag_failure(self, mock_popen, mock_production, mock_config):
        """Test DAG building failure."""
        # Mock failed bayeswave_pipe execution
        mock_process = Mock()
        mock_process.communicate.return_value = (b"Error occurred", b"stderr")
        mock_popen.return_value = mock_process

        mock_ini = MagicMock()
        mock_ini._get_user = Mock(return_value="test.user")
        mock_ini.ini_loc = "/tmp/test.ini"
        mock_production.get_configuration.return_value = mock_ini

        pipeline = BayesWave(mock_production)

        with pytest.raises(PipelineException, match="DAG file could not be created"):
            pipeline.build_dag(user="test.user", dryrun=False)

    def test_build_dag_dryrun(self, mock_production, mock_config, capsys):
        """Test DAG building in dryrun mode."""
        mock_ini = MagicMock()
        mock_ini._get_user = Mock(return_value="test.user")
        mock_ini.ini_loc = "/tmp/test.ini"
        mock_production.get_configuration.return_value = mock_ini

        pipeline = BayesWave(mock_production)
        pipeline.build_dag(user="test.user", dryrun=True)

        captured = capsys.readouterr()
        assert "bayeswave_pipe" in captured.out


class TestSubmitDag:
    """Test DAG submission."""

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    @patch("asimov_bayeswave.bayeswave.set_directory")
    def test_submit_dag_success(
        self, mock_set_dir, mock_glob, mock_popen, mock_production, mock_config
    ):
        """Test successful DAG submission."""
        # Mock glob to return empty lists (no files to modify)
        mock_glob.return_value = []

        # Mock successful condor_submit_dag
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"submitted to cluster 12345",
            b"",
        )
        mock_popen.return_value = mock_process

        pipeline = BayesWave(mock_production)
        result = pipeline.submit_dag(dryrun=False)

        assert result == (12345,)
        assert mock_production.job_id == 12345
        assert mock_production.status == "running"

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    @patch("asimov_bayeswave.bayeswave.set_directory")
    def test_submit_dag_failure(
        self, mock_set_dir, mock_glob, mock_popen, mock_production, mock_config
    ):
        """Test DAG submission failure."""
        mock_glob.return_value = []

        # Mock failed condor_submit_dag
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"Error: submission failed",
            b"stderr",
        )
        mock_popen.return_value = mock_process

        pipeline = BayesWave(mock_production)

        with pytest.raises(PipelineException, match="DAG file could not be submitted"):
            pipeline.submit_dag(dryrun=False)


class TestBeforeSubmit:
    """Test pre-submission modifications."""

    @patch("builtins.open", new_callable=mock_open, read_data="original content")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_before_submit_adds_disk_request(
        self, mock_glob, mock_file, mock_production, mock_config
    ):
        """Test that request_disk is added to submission files."""
        mock_glob.side_effect = [
            ["/tmp/test.sub"],  # First call for .sub files
            [],  # Second call for .py files
        ]

        pipeline = BayesWave(mock_production)
        pipeline.before_submit()

        # Check that file was opened for reading and writing
        assert mock_file.call_count >= 2

    @patch("builtins.open", new_callable=mock_open, read_data="original content")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_before_submit_fixes_shebang(
        self, mock_glob, mock_file, mock_production, mock_config
    ):
        """Test that Python shebang is fixed."""
        mock_glob.side_effect = [
            [],  # First call for .sub files
            ["/tmp/test.py"],  # Second call for .py files
        ]

        pipeline = BayesWave(mock_production)
        pipeline.before_submit()

        # Verify file operations occurred
        assert mock_file.call_count >= 2


class TestCollectAssets:
    """Test asset collection."""

    @patch("asimov_bayeswave.bayeswave.os.path.exists")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_collect_assets_psds(
        self, mock_glob, mock_exists, mock_production, mock_config
    ):
        """Test PSD collection."""
        # Mock glob to return PSD files
        mock_glob.return_value = [
            "/tmp/test_rundir/trigtime_123/post/clean/glitch_median_PSD_forLI_H1.dat"
        ]
        mock_exists.return_value = True

        pipeline = BayesWave(mock_production)
        assets = pipeline.collect_assets()

        assert "psds" in assets
        assert "xml psds" in assets
        assert "H1" in assets["psds"]

    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_collect_assets_no_psds(self, mock_glob, mock_production, mock_config):
        """Test asset collection with no PSDs."""
        mock_glob.return_value = []

        pipeline = BayesWave(mock_production)
        assets = pipeline.collect_assets()

        assert "psds" in assets
        assert len(assets["psds"]) == 0


class TestDetectCompletion:
    """Test completion detection."""

    @patch("asimov_bayeswave.bayeswave.BayesWave.collect_assets")
    def test_detect_completion_success(
        self, mock_collect, mock_production, mock_config
    ):
        """Test successful completion detection."""
        mock_collect.return_value = {"psds": {"H1": "/path/to/psd.dat"}}

        pipeline = BayesWave(mock_production)
        assert pipeline.detect_completion() is True

    @patch("asimov_bayeswave.bayeswave.BayesWave.collect_assets")
    def test_detect_completion_no_psds(
        self, mock_collect, mock_production, mock_config
    ):
        """Test completion detection with no PSDs."""
        mock_collect.return_value = {"psds": {}}

        pipeline = BayesWave(mock_production)
        assert pipeline.detect_completion() is False


class TestSupressPsd:
    """Test PSD suppression."""

    @patch("asimov_bayeswave.bayeswave.np.savetxt")
    @patch("asimov_bayeswave.bayeswave.np.genfromtxt")
    @patch("asimov_bayeswave.bayeswave.copyfile")
    @patch("asimov_bayeswave.bayeswave.Store")
    def test_supress_psd(
        self,
        mock_store,
        mock_copy,
        mock_genfromtxt,
        mock_savetxt,
        mock_production,
        mock_config,
    ):
        """Test PSD suppression functionality."""
        # Create mock PSD data
        freq = np.linspace(10, 100, 100)
        psd = np.ones_like(freq) * 1e-23
        mock_psd_data = np.column_stack((freq, psd))
        mock_genfromtxt.return_value = mock_psd_data

        # Mock store
        mock_store_instance = MagicMock()
        mock_store.return_value = mock_store_instance

        pipeline = BayesWave(mock_production)
        pipeline.supress_psd("H1", 60.0, 60.5)

        # Verify suppression was applied
        assert mock_savetxt.called
        call_args = mock_savetxt.call_args
        suppressed_data = call_args[0][1]

        # Check that frequencies in the suppression range have PSD = 1.0
        freq_mask = (suppressed_data[:, 0] >= 60.0) & (suppressed_data[:, 0] <= 60.5)
        assert np.all(suppressed_data[freq_mask, 1] == 1.0)


class TestConvertPsd:
    """Test PSD conversion to XML."""

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    def test_convert_psd_success(self, mock_popen, mock_production, mock_config):
        """Test successful PSD conversion."""
        mock_process = Mock()
        mock_process.communicate.return_value = (b"Conversion successful", None)
        mock_popen.return_value = mock_process

        mock_production.event.repository.add_file = Mock()

        pipeline = BayesWave(mock_production)
        pipeline._convert_psd("/path/to/psd.dat", "H1")

        assert mock_popen.called
        call_args = mock_popen.call_args[0][0]
        assert "convert_psd_ascii2xml" in call_args

    @patch("asimov_bayeswave.bayeswave.subprocess.Popen")
    def test_convert_psd_failure(self, mock_popen, mock_production, mock_config):
        """Test PSD conversion failure."""
        mock_process = Mock()
        mock_process.communicate.return_value = (b"output", b"error message")
        mock_popen.return_value = mock_process

        pipeline = BayesWave(mock_production)

        with pytest.raises(Exception, match="XML format PSD could not be created"):
            pipeline._convert_psd("/path/to/psd.dat", "H1")


class TestResurrect:
    """Test job resurrection."""

    @patch("asimov_bayeswave.bayeswave.BayesWave.submit_dag")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_resurrect_with_rescue_files(
        self, mock_glob, mock_submit, mock_production, mock_config
    ):
        """Test resurrection with rescue files."""
        mock_glob.return_value = ["rescue001", "rescue002"]

        pipeline = BayesWave(mock_production)
        pipeline.resurrect()

        assert mock_submit.called

    @patch("asimov_bayeswave.bayeswave.BayesWave.submit_dag")
    @patch("asimov_bayeswave.bayeswave.glob.glob")
    def test_resurrect_too_many_attempts(
        self, mock_glob, mock_submit, mock_production, mock_config
    ):
        """Test resurrection fails after too many attempts."""
        mock_glob.return_value = [f"rescue{i:03d}" for i in range(1, 6)]

        pipeline = BayesWave(mock_production)
        pipeline.resurrect()

        assert not mock_submit.called


class TestHtml:
    """Test HTML output generation."""

    def test_html_finished_status(self, mock_production, mock_config):
        """Test HTML generation for finished job."""
        mock_production.status = "finished"

        pipeline = BayesWave(mock_production)
        html = pipeline.html()

        assert "asimov-pipeline" in html
        assert "Megaplot" in html
        assert mock_production.name in html

    def test_html_running_status(self, mock_production, mock_config):
        """Test HTML generation for running job."""
        mock_production.status = "running"

        pipeline = BayesWave(mock_production)
        html = pipeline.html()

        assert html == ""


def test_module_imports():
    """Test that the module imports correctly."""
    from asimov_bayeswave import BayesWave, __version__

    assert BayesWave is not None
    assert __version__ is not None

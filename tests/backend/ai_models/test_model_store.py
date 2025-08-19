import pytest
import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Assuming ModelStore is located at backend/ai_models/model_store.py
# Adjust import path if necessary
from backend.ai_models.model_store import ModelStore

# Mock the PROJECT_ROOT and MODELS_BASE_DIR for testing
# This ensures tests don't interfere with actual project directories
@pytest.fixture(autouse=True)
def mock_project_root(tmp_path, monkeypatch):
    mock_root = tmp_path / "mock_project_root"
    mock_root.mkdir()
    
    mock_models_base_dir = mock_root / "models"
    mock_models_base_dir.mkdir()

    monkeypatch.setattr("backend.ai_models.model_store.PROJECT_ROOT", mock_root)
    monkeypatch.setattr("backend.ai_models.model_store.MODELS_BASE_DIR", mock_models_base_dir)
    
    # Ensure the ModelStore instance uses the mocked paths
    monkeypatch.setattr("backend.ai_models.model_store.model_store", ModelStore())
    
    return mock_root

@pytest.fixture
def model_store_instance():
    return ModelStore()

@pytest.fixture
def setup_model_paths(mock_project_root):
    provider = "test_provider"
    model_name = "test_model"
    
    model_path = mock_project_root / "models" / provider / model_name
    versions_path = model_path / "versions"
    history_path = model_path / "history.json"
    active_pointer_path = model_path / "active"
    
    model_path.mkdir(parents=True, exist_ok=True)
    versions_path.mkdir(exist_ok=True)
    
    return {
        "provider": provider,
        "model_name": model_name,
        "model_path": model_path,
        "versions_path": versions_path,
        "history_path": history_path,
        "active_pointer_path": active_pointer_path
    }

def create_dummy_version(versions_path: Path, version_tag: str, content: str = "dummy_content"):
    version_dir = versions_path / version_tag
    version_dir.mkdir(parents=True, exist_ok=True)
    (version_dir / "file.txt").write_text(content)
    return version_dir

def test_prepare_staging_creates_version_dir_and_does_not_change_active(model_store_instance, setup_model_paths, tmp_path):
    provider = setup_model_paths["provider"]
    model_name = setup_model_paths["model_name"]
    versions_path = setup_model_paths["versions_path"]
    active_pointer_path = setup_model_paths["active_pointer_path"]
    
    version_tag = "v1.0.0"
    src_path = tmp_path / "source_model"
    src_path.mkdir()
    (src_path / "model_file.bin").write_text("binary_data")

    # Ensure active pointer does not exist initially
    assert not active_pointer_path.exists()

    staging_path = model_store_instance.prepare_staging(provider, model_name, version_tag, src_path)

    # Check if staging directory is created and contains content
    assert staging_path.exists()
    assert (staging_path / "model_file.bin").exists()
    assert staging_path.parent == versions_path

    # Check that active pointer is still not created/changed
    assert not active_pointer_path.exists()

def test_activate_atomic_swap_and_history_append(model_store_instance, setup_model_paths, monkeypatch):
    provider = setup_model_paths["provider"]
    model_name = setup_model_paths["model_name"]
    versions_path = setup_model_paths["versions_path"]
    history_path = setup_model_paths["history_path"]
    active_pointer_path = setup_model_paths["active_pointer_path"]

    # Create a dummy version to activate
    version_tag = "v1.0.0"
    create_dummy_version(versions_path, version_tag)

    metadata = {"user": "test_user", "env": "dev"}
    
    # Mock sys.platform to ensure symlink path is taken (for non-Windows)
    monkeypatch.setattr(os, "getenv", lambda x: None) # Ensure PYTHON_SYMLINK_ADMIN is not set
    monkeypatch.setattr(sys, "platform", "linux")

    model_store_instance.activate(provider, model_name, version_tag, metadata)

    # Check atomic swap (symlink created)
    assert active_pointer_path.is_symlink()
    assert os.readlink(active_pointer_path) == str(versions_path / version_tag)

    # Check history.json append
    assert history_path.exists()
    history = json.loads(history_path.read_text())
    assert len(history) == 1
    assert history[0]["version_tag"] == version_tag
    assert "checksum" in history[0]
    assert "activated_at" in history[0]
    assert history[0]["metadata"] == metadata

    # Activate a second version
    version_tag_2 = "v1.0.1"
    create_dummy_version(versions_path, version_tag_2, "new_content")
    model_store_instance.activate(provider, model_name, version_tag_2)

    # Check symlink updated
    assert os.readlink(active_pointer_path) == str(versions_path / version_tag_2)
    
    # Check history updated
    history = json.loads(history_path.read_text())
    assert len(history) == 2
    assert history[1]["version_tag"] == version_tag_2

def test_activate_windows_pointer_fallback(model_store_instance, setup_model_paths, monkeypatch):
    provider = setup_model_paths["provider"]
    model_name = setup_model_paths["model_name"]
    versions_path = setup_model_paths["versions_path"]
    history_path = setup_model_paths["history_path"]
    active_pointer_path = setup_model_paths["active_pointer_path"] # This will be active.json

    # Create a dummy version to activate
    version_tag = "v1.0.0"
    create_dummy_version(versions_path, version_tag)

    # Mock sys.platform to simulate Windows without symlink admin
    monkeypatch.setattr(os, "getenv", lambda x: "0" if x == "PYTHON_SYMLINK_ADMIN" else None)
    monkeypatch.setattr(sys, "platform", "win32")

    model_store_instance.activate(provider, model_name, version_tag)

    # Check active.json created
    active_json_path = active_pointer_path.with_suffix(".json")
    assert active_json_path.exists()
    active_data = json.loads(active_json_path.read_text())
    assert active_data["active_version_tag"] == version_tag
    assert active_data["active_path"] == str(versions_path / version_tag)
    assert "checksum" in active_data
    assert "activated_at" in active_data

    # Check history.json append
    assert history_path.exists()
    history = json.loads(history_path.read_text())
    assert len(history) == 1
    assert history[0]["version_tag"] == version_tag

def test_rollback_switches_back_and_validates_checksum(model_store_instance, setup_model_paths, monkeypatch):
    provider = setup_model_paths["provider"]
    model_name = setup_model_paths["model_name"]
    versions_path = setup_model_paths["versions_path"]
    history_path = setup_model_paths["history_path"]
    active_pointer_path = setup_model_paths["active_pointer_path"]

    # Mock sys.platform to ensure symlink path is taken (for non-Windows)
    monkeypatch.setattr(os, "getenv", lambda x: None) # Ensure PYTHON_SYMLINK_ADMIN is not set
    monkeypatch.setattr(sys, "platform", "linux")

    # Activate initial version (v1.0.0)
    version_1_tag = "v1.0.0"
    create_dummy_version(versions_path, version_1_tag, "content_v1")
    model_store_instance.activate(provider, model_name, version_1_tag)
    assert os.readlink(active_pointer_path) == str(versions_path / version_1_tag)

    # Activate a second version (v1.0.1)
    version_2_tag = "v1.0.1"
    create_dummy_version(versions_path, version_2_tag, "content_v2")
    model_store_instance.activate(provider, model_name, version_2_tag)
    assert os.readlink(active_pointer_path) == str(versions_path / version_2_tag)

    # Perform rollback to v1.0.0
    model_store_instance.rollback(provider, model_name, version_1_tag)

    # Check if symlink points to v1.0.0
    assert os.readlink(active_pointer_path) == str(versions_path / version_1_tag)

    # Check history updated with rollback entry
    history = json.loads(history_path.read_text())
    assert len(history) == 3 # v1.0.0 activation, v1.0.1 activation, v1.0.0 rollback
    assert history[2]["version_tag"] == version_1_tag
    assert history[2]["metadata"]["action"] == "rollback"
    assert history[2]["metadata"]["rolled_back_from"] == version_2_tag

    # Test rollback with checksum mismatch (simulate tampering)
    tampered_version_dir = versions_path / version_1_tag
    (tampered_version_dir / "file.txt").write_text("tampered_content") # Change content to alter checksum

    with pytest.raises(ValueError, match="Checksum mismatch for rollback target"):
        model_store_instance.rollback(provider, model_name, version_1_tag)

def test_prune_keeps_most_recent_versions_and_active(model_store_instance, setup_model_paths, monkeypatch):
    provider = setup_model_paths["provider"]
    model_name = setup_model_paths["model_name"]
    versions_path = setup_model_paths["versions_path"]
    active_pointer_path = setup_model_paths["active_pointer_path"]

    # Mock sys.platform to ensure symlink path is taken (for non-Windows)
    monkeypatch.setattr(os, "getenv", lambda x: None) # Ensure PYTHON_SYMLINK_ADMIN is not set
    monkeypatch.setattr(sys, "platform", "linux")

    # Create and activate several versions
    versions = ["v0.9.0", "v1.0.0", "v1.0.1", "v1.0.2", "v1.1.0"]
    for i, tag in enumerate(versions):
        create_dummy_version(versions_path, tag, f"content_{tag}")
        # Simulate different activation times for sorting
        mock_time = datetime.now() - timedelta(days=len(versions) - i)
        monkeypatch.setattr(datetime, "now", lambda: mock_time)
        model_store_instance.activate(provider, model_name, tag)
    
    # Current active version is v1.1.0
    assert model_store_instance.current(provider, model_name)["version_tag"] == "v1.1.0"

    # Prune, keeping 3 versions
    model_store_instance.prune(provider, model_name, keep=3)

    # Check which versions remain
    remaining_versions = [d.name for d in versions_path.iterdir() if d.is_dir()]
    
    # The active version (v1.1.0) should always be kept
    # The 3 most recent activated versions should be kept (v1.0.1, v1.0.2, v1.1.0)
    # So, v1.1.0, v1.0.2, v1.0.1 should remain.
    expected_kept_versions = {"v1.1.0", "v1.0.2", "v1.0.1"}
    assert set(remaining_versions) == expected_kept_versions
    
    # Ensure older versions are deleted
    assert not (versions_path / "v0.9.0").exists()
    assert not (versions_path / "v1.0.0").exists()

    # Test prune when active version is one of the older ones (e.g., after rollback)
    model_store_instance.rollback(provider, model_name, "v1.0.0") # Rollback to an older version
    assert model_store_instance.current(provider, model_name)["version_tag"] == "v1.0.0"
    
    # Create a new version after rollback
    create_dummy_version(versions_path, "v1.2.0", "content_v1.2.0")
    model_store_instance.activate(provider, model_name, "v1.2.0")

    # Prune again, keeping 3
    model_store_instance.prune(provider, model_name, keep=3)
    
    remaining_versions_after_rollback_prune = [d.name for d in versions_path.iterdir() if d.is_dir()]
    # Active (v1.2.0) + 2 most recent from history (v1.1.0, v1.0.2)
    expected_kept_versions_after_rollback_prune = {"v1.2.0", "v1.1.0", "v1.0.2"}
    assert set(remaining_versions_after_rollback_prune) == expected_kept_versions_after_rollback_prune

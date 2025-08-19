import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import os

# Adjust import paths if necessary
from backend.ai_health.rollback import should_rollback, perform_rollback
from backend.ai_models.model_store import ModelStore # To mock its methods
from backend.notifications.admin_notify import send_admin_notification # To mock it

# Mock ModelStore and send_admin_notification globally for tests
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('backend.ai_health.rollback.model_store', autospec=True) as mock_model_store, \
         patch('backend.ai_health.rollback._read_model_history', autospec=True) as mock_read_history, \
         patch('backend.notifications.admin_notify.send_admin_notification', autospec=True) as mock_send_notification:
        yield mock_model_store, mock_read_history, mock_send_notification

# Test should_rollback function
@pytest.mark.parametrize("agg_metrics, thresholds, expected_rollback", [
    # Error rate breach
    ({"error_rate": 0.15, "success_rate": 0.9, "avg_response_time": 5.0}, {"error_rate_threshold": 0.1, "min_success_rate": 0.8, "max_avg_response_time": 10.0}, True),
    # Success rate breach
    ({"error_rate": 0.05, "success_rate": 0.8, "avg_response_time": 5.0}, {"error_rate_threshold": 0.1, "min_success_rate": 0.9, "max_avg_response_time": 10.0}, True),
    # Avg response time breach
    ({"error_rate": 0.05, "success_rate": 0.9, "avg_response_time": 12.0}, {"error_rate_threshold": 0.1, "min_success_rate": 0.8, "max_avg_response_time": 10.0}, True),
    # No breach (healthy)
    ({"error_rate": 0.05, "success_rate": 0.95, "avg_response_time": 5.0}, {"error_rate_threshold": 0.1, "min_success_rate": 0.9, "max_avg_response_time": 10.0}, False),
    # Edge case: exactly on threshold (should not trigger)
    ({"error_rate": 0.1, "success_rate": 0.9, "avg_response_time": 10.0}, {"error_rate_threshold": 0.1, "min_success_rate": 0.9, "max_avg_response_time": 10.0}, False),
])
def test_should_rollback(agg_metrics, thresholds, expected_rollback):
    assert should_rollback(agg_metrics, thresholds) == expected_rollback

# Test perform_rollback function
def test_perform_rollback_success(mock_dependencies):
    mock_model_store, mock_read_history, mock_send_notification = mock_dependencies
    
    provider = "test_provider"
    model_name = "test_model"
    current_tag = "v2.0.0"
    last_known_good_tag = "v1.0.0"

    mock_model_store.current.return_value = {"version_tag": current_tag}
    mock_read_history.return_value = [
        {"version_tag": "v2.0.0", "activated_at": (datetime.now() - timedelta(minutes=1)).isoformat(), "checksum": "abc"},
        {"version_tag": "v1.0.0", "activated_at": (datetime.now() - timedelta(minutes=5)).isoformat(), "checksum": "xyz"}
    ]
    mock_model_store.rollback.return_value = None # rollback method doesn't return anything

    rolled_back_tag = perform_rollback(provider, model_name, dry_run=False)

    mock_model_store.current.assert_called_once_with(provider, model_name)
    mock_read_history.assert_called_once_with(provider, model_name)
    mock_model_store.rollback.assert_called_once_with(provider, model_name, last_known_good_tag)
    assert rolled_back_tag == last_known_good_tag

def test_perform_rollback_no_suitable_version(mock_dependencies):
    mock_model_store, mock_read_history, mock_send_notification = mock_dependencies
    
    provider = "test_provider"
    model_name = "test_model"
    current_tag = "v1.0.0"

    mock_model_store.current.return_value = {"version_tag": current_tag}
    mock_read_history.return_value = [
        {"version_tag": "v1.0.0", "activated_at": (datetime.now() - timedelta(minutes=1)).isoformat(), "checksum": "abc"}
    ] # Only current version in history

    rolled_back_tag = perform_rollback(provider, model_name, dry_run=False)

    mock_model_store.current.assert_called_once_with(provider, model_name)
    mock_read_history.assert_called_once_with(provider, model_name)
    mock_model_store.rollback.assert_not_called() # Should not attempt rollback
    assert rolled_back_tag is None

def test_perform_rollback_dry_run(mock_dependencies):
    mock_model_store, mock_read_history, mock_send_notification = mock_dependencies
    
    provider = "test_provider"
    model_name = "test_model"
    current_tag = "v2.0.0"
    last_known_good_tag = "v1.0.0"

    mock_model_store.current.return_value = {"version_tag": current_tag}
    mock_read_history.return_value = [
        {"version_tag": "v2.0.0", "activated_at": (datetime.now() - timedelta(minutes=1)).isoformat(), "checksum": "abc"},
        {"version_tag": "v1.0.0", "activated_at": (datetime.now() - timedelta(minutes=5)).isoformat(), "checksum": "xyz"}
    ]

    rolled_back_tag = perform_rollback(provider, model_name, dry_run=True)

    mock_model_store.rollback.assert_not_called() # Should not attempt rollback in dry run
    assert rolled_back_tag == last_known_good_tag

def test_perform_rollback_rollback_exception(mock_dependencies):
    mock_model_store, mock_read_history, mock_send_notification = mock_dependencies
    
    provider = "test_provider"
    model_name = "test_model"
    current_tag = "v2.0.0"
    last_known_good_tag = "v1.0.0"

    mock_model_store.current.return_value = {"version_tag": current_tag}
    mock_read_history.return_value = [
        {"version_tag": "v2.0.0", "activated_at": (datetime.now() - timedelta(minutes=1)).isoformat(), "checksum": "abc"},
        {"version_tag": "v1.0.0", "activated_at": (datetime.now() - timedelta(minutes=5)).isoformat(), "checksum": "xyz"}
    ]
    mock_model_store.rollback.side_effect = Exception("Simulated rollback error")

    rolled_back_tag = perform_rollback(provider, model_name, dry_run=False)

    mock_model_store.rollback.assert_called_once_with(provider, model_name, last_known_good_tag)
    assert rolled_back_tag is None # Should return None on exception

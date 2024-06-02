from unittest.mock import Mock

def create_mock_terminal_size():
    """Create a mock terminal size with 80 columns."""
    mock_size = Mock()
    mock_size.columns = 80
    return mock_size

def assert_non_empty_string(value):
    """Assert that the value is a non-empty string."""
    assert isinstance(value, str)
    assert value != ""

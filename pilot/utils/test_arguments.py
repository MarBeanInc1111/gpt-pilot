import pytest
from unittest.mock import patch, mock_open
import uuid
from .arguments import get_email, username_to_uuid

@pytest.fixture
def mock_file_content(mocker):
    mock_file_content = """\
    [user]\n\
        name = test_user\n\
        email = test@example.com\n"""
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('builtins.open', mock_open(read_data=mock_file_content))
    return mock_file_content

def test_email_found_in_gitconfig(mock_file_content):
    assert get_email() == "test@example.com"

@pytest.fixture
def mock_file_content_no_email(mocker):
    mock_file_content = """\
    [user]\n\
        name = test_user\n"""
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('builtins.open', mock_open(read_data=mock_file_content))
    return mock_file_content

@pytest.fixture
def mock_uuid():
    return "12345678-1234-5678-1234-567812345678"

def test_email_not_found_in_gitconfig(mock_file_content_no_email, mock_uuid):
    with patch.object(uuid, "uuid4", return_value=mock_uuid):
        assert get_email() == mock_uuid

def test_gitconfig_not_present(mocker, mock_uuid):
    mocker.patch('os.path.exists', return_value=False)
    with patch.object(uuid, "uuid4", return_value=mock_uuid):
        assert get_email() == mock_uuid

@pytest.fixture
def expected_uuid():
    return "31676025-316f-b555-e0bf-a12f0bcfd0ea"

def test_username_to_uuid(expected_uuid):
    assert username_to_uuid("test_user") == expected_uuid

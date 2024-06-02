import os
from unittest.mock import patch, PropertyMock

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

from main import get_custom_print
from helpers.AgentConvo import AgentConvo
from helpers.cli import execute_command
from helpers.test_Project import create_project
from helpers.technology import ENVIRONMENT_SETUP_STEP
from utils.llm_connection import requests

from .Developer import Developer


@pytest.fixture
def project_fixture():
    return create_project()


@pytest.fixture
def get_custom_print_fixture():
    return get_custom_print({})


class TestDeveloper:
    @pytest.mark.usefixtures("project_fixture", "get_custom_print_fixture")
    @patch('helpers.AgentConvo.save_development_step')
    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "python --version", "timeout": 10}'})
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))
    def test_install_technology(self, mock_execute_command, mock_completion, mock_save, developer):
        # Given
        developer.convo_os_specific_tech = AgentConvo(developer)

        # When
        llm_response = developer.check_system_dependency('python')

        # Then
        assert llm_response == 'DONE'
        mock_execute_command.assert_called_once_with(developer.project, 'python --version', timeout=10, command_id=None)

    @pytest.mark.usefixtures("project_fixture", "get_custom_print_fixture")
    @patch('helpers.AgentConvo.save_development_step')
    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"tasks": [{"command": "ls -al"}]}'})
    def test_implement_task(self, mock_completion, mock_save, developer):
        # Given any project
        project = developer.project
        project.project_description = 'Test Project'
        project.development_plan = [{'description': 'Do stuff', 'user_review_goal': 'Do stuff'}]
        project.get_all_coded_files = lambda: []
        project.current_step = 'test'

        # and a developer who will execute any task
        developer.execute_task = MagicMock()
        developer.execute_task.return_value = {'success': True}

        # When
        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        # Then we parse the response correctly and send list of steps to execute_task
        assert developer.execute_task.call_count == 1
        assert developer.execute_task.call_args[0][1] == [{'command': 'ls -al'}]

    # ... (other test methods follow the same pattern)

@pytest.fixture
def developer(project_fixture, get_custom_print_fixture):
    builtins.print, ipc_client_instance = get_custom_print_fixture
    name = 'TestDeveloper'
    project = project_fixture
    project.app_id = 'test-developer'
    project.name = name
    project.set_root_path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                          '../../../workspace/TestDeveloper')))
    project.technologies = []
    project.current_step = ENVIRONMENT_SETUP_STEP
    return Developer(project)

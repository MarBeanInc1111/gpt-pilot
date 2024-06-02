import pytest
from unittest.mock import patch

from helpers.AgentConvo import AgentConvo
from helpers.agents import Developer
from helpers.cli import terminate_running_processes
from helpers.utils import create_project

class MockQuestionary:
    def __init__(self, answers):
        self.answers = answers
    
    def ask(self, question):


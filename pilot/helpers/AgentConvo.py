import json
import re
from os.path import sep
from typing import Any, Dict, List

import logging

class AgentConvo:
    """
    Represents a conversation with an agent.

    Args:
        agent: An instance of the agent participating in the conversation.
    """

    def __init__(self, agent, temperature: float = 0.7):
        self.messages: List[Dict[str, str]] = []
        self.branches = {}
        self.log_to_user = True
        self.agent = agent
        self.high_level_step = self.agent.project.current_step
        self.temperature = temperature

        # add system message
        system_message = {
            "role": "system",
            "content": self.get_sys_message(self.agent.role, self.agent.project.args),
        }
        logger.info(
            "\n>>>>>>>>>> System Prompt >>>>>>>>>>\n%s\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",
            system_message["content"],
        )
        self.messages.append(system_message)

    def get_sys_message(self, role: str, args: Any) -> str:
        # Implement this method based on the original 'get_sys_message' function.
        pass

    def send_message(
        self,
        prompt_path: str = None,
        prompt_data: Dict[str, Any] = None,
        function_calls: Any = None,
        should_log_message: bool = True,
    ) -> Dict[str, Any]:
        # ... (rest of the code)

    def format_message_content(self, response: Any, function_calls: Any) -> str:
        # ... (rest of the code)

    def continuous_conversation(
        self, prompt_path: str, prompt_data: Dict[str, Any], function_calls: Any = None
    ) -> List[Any]:
        # ... (rest of the code)

    def save_branch(self, branch_name: str = None) -> str:
        # ... (rest of the code)

    def load_branch(self, branch_name: str, reload_files: bool = True) -> None:
        # ... (rest of the code)

    def replace_files(self) -> None:
        # ... (rest of the code)

    def replace_files_in_one_message(self, files: Any, message: str) -> str:
        # ... (rest of the code)

    @staticmethod
    def escape_specials(s: str) -> str:
        # ... (rest of the code)

    def convo_length(self) -> int:
        # ... (rest of the code)

    def log_message(self, content: str) -> None:
        # ... (rest of the code)

    def to_context_prompt(self) -> str:
        # ... (rest of the code)

    def to_playground(self) -> None:
        # ... (rest of the code)

    def remove_last_x_messages(self, x: int) -> None:
        # ... (rest of the code)

    def construct_and_add_message_from_prompt(
        self, prompt_path: str, prompt_data: Dict[str, Any]
    ) -> None:
        # ... (rest of the code)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
)
logger = logging.getLogger()

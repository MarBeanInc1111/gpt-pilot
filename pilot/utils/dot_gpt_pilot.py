import os
import datetime
import json
import yaml
from dotenv import load_dotenv if "dotenv" in globals() else None


class DotGptPilot:
    """
    Manages the `.gpt-pilot` directory.
    """

    def __init__(self, log_chat_completions: bool = True):
        self.log_chat_completions = log_chat_completions
        self.dot_gpt_pilot_path = self.with_root_path("~")
        self.chat_log_path = None

    def with_root_path(self, root_path: str, create=True) -> str:
        """
        Sets the root path for the `.gpt-pilot` directory.

        :param root_path: The root path.
        :param create: Whether to create the directory if it doesn't exist.
        :return: The expanded directory path.
        """
        dot_gpt_pilot_path = os.path.expanduser(os.path.join(root_path, ".gpt-pilot"))
        if create and self.log_chat_completions and not os.path.exists(dot_gpt_pilot_path):
            os.makedirs(dot_gpt_pilot_path)
        self.dot_gpt_pilot_path = dot_gpt_pilot_path
        return dot_gpt_pilot_path

    def chat_log_folder(self, task=None) -> str:
        """
        Sets the chat log folder path.

        :param task: The task number.
        :return: The chat log folder path.
        """
        chat_log_path = os.path.join(self.dot_gpt_pilot_path, "chat_log")
        if task is not None:
            chat_log_path = os.path.join(chat_log_path, f"task_{task}")
        os.makedirs(chat_log_path, exist_ok=True)
        self.chat_log_path = chat_log_path
        return chat_log_path

    def log_chat_completion(self, endpoint: str, model: str, req_type: str, messages: list[dict], response: str) -> None:
        """
        Logs a chat completion.

        :param endpoint: The endpoint.
        :param model: The model.
        :param req_type: The request type.
        :param messages: The messages.
        :param response: The response.
        :return: None
        """
        if not self.log_chat_completions:
            return
        time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        file_path = os.path.join(self.chat_log_path, f"{time}-{req_type}.yaml")
        data = {
            "endpoint": endpoint,
            "model": model,
            "messages": messages,
            "response": response,
        }
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, width=120, indent=2, default_flow_style=False, sort_keys=False)

    def log_chat_completion_json(self, endpoint: str, model: str, req_type: str, functions: dict, json_response: str) -> None:
        """
        Logs a chat completion in JSON format.

        :param endpoint: The endpoint.
        :param model: The model.
        :param req_type: The request type.
        :param functions: The functions.
        :param json_response: The JSON response.
        :return: None
        """
        if not self.log_chat_completions:
            return
        time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        file_path = os.path.join(self.chat_log_path, f"{time}-{req_type}.json")
        data = {
            "endpoint": endpoint,
            "model": model,
            "functions": functions,
            "response": json.loads(json_response),
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        :return: The string representation.
        """
        return f"DotPilotGpt(dot_gpt_pilot_path='{self.dot_gpt_pilot_path}', chat_log_path='{self.chat_log_path}')"


if __name__ == "__main__":
    load_dotenv()
    dot_gpt_pilot = DotGptPilot()
    print(dot_gpt_pilot)

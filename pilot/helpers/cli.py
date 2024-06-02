import psutil
import subprocess
import os
import signal
import threading
import queue
import time
import platform
from typing import Dict, Union, Any, Optional, List, Tuple, Callable

import colorama
from logger.logger import logger
from utils.style import color_green, color_red, color_yellow_bold
from utils.ignore import IgnoreMatcher
from database.database import save_command_run
from helpers.exceptions import TooDeepRecursionError, TokenLimitError, CommandFinishedEarly
from prompts.prompts import ask_user
from const.code_execution import MIN_COMMAND_RUN_TIME, MAX_COMMAND_RUN_TIME, MAX_COMMAND_OUTPUT_LENGTH
from const.messages import AFFIRMATIVE_ANSWERS, NEGATIVE_ANSWERS

colorama.init()

interrupted = False

RunningProcessesType = Dict[str, Tuple[str, int]]


def enqueue_output(out: subprocess.PIPE, q: queue.Queue) -> None:
    # ... (same as before)


def run_command(command: str, root_path: str, q_stdout: queue.Queue, q_stderr: queue.Queue) -> subprocess.Popen:
    # ... (same as before)


def terminate_named_process(command_id: str) -> None:
    # ... (same as before)


def terminate_running_processes() -> None:
    # ... (same as before)


def term_proc_windows(pid: int) -> None:
    # ... (same as before)


def term_proc_unix_like(pid: int) -> None:
    # ... (same as before)


def is_process_running(pid: int) -> bool:
    # ... (same as before)


def terminate_process(pid: int, name: Optional[str] = None) -> None:
    # ... (same as before)


def read_queue_line(q: queue.Queue, stdout: bool = True) -> str:
    # ... (same as before)


def read_remaining_queue(q: queue.Queue, stdout: bool = True) -> str:
    # ... (same as before)


def execute_command(project, command: str, timeout: Optional[int] = None,
                    success_message: Optional[str] = None, command_id: Optional[str] = None,
                    force: bool = False) -> Tuple[Optional[str], Optional[str], int]:
    # ... (same as before)


def check_if_command_successful(convo: Any, command: str, cli_response: Optional[str],
                                response: Optional[str], exit_code: int,
                                additional_message: Optional[str] = None,
                                task_steps: Optional[List[str]] = None, step_index: Optional[int] = None) -> str:
    # ... (same as before)


def build_directory_tree(path: str, prefix: str = '', root_path: Optional[str] = None) -> str:
    # ... (same as before)


def execute_command_and_check_cli_response(convo: Any, command: dict,
                                           task_steps: Optional[List[str]] = None, step_index: Optional[int] = None) -> Tuple[Optional[str], str]:
    # ... (same as before)



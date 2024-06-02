import platform
import uuid
import re
import traceback
from typing import Any, Dict, List, Optional

from const.code_execution import MAX_COMMAND_DEBUG_TRIES, MAX_RECURSION_LAYER
from const.function_calls import DEBUG_STEPS_BREAKDOWN
from const.messages import AFFIRMATIVE_ANSWERS, NEGATIVE_ANSWERS
from helpers.AgentConvo import AgentConvo
from helpers.exceptions import TokenLimitError
from helpers.exceptions import TooDeepRecursionError
from logger.logger import logger
from prompts.prompts import ask_user
from utils.exit import trace_code_event
from utils.print import print_task_progress

class Debugger:
    def __init__(self, agent):
        self.agent = agent
        self.recursion_layer = 0

    def debug(self, convo: AgentConvo, command: Optional[Dict[str, Any]] = None, user_input: Optional[str] = None,
              issue_description: Optional[str] = None, is_root_task: bool = False,
              ask_before_debug: bool = False, task_steps: Optional[List[str]] = None, step_index: Optional[int] = None) -> bool:
        """
        Debug a conversation.

        Args:
            convo (AgentConvo): The conversation object.
            command (dict, optional): The command to debug. Default is None.
            user_input (str, optional): User input for debugging. Default is None.
                Should provide `command` or `user_input`.
            issue_description (str, optional): Description of the issue to debug. Default is None.
            ask_before_debug (bool, optional): True if we have to ask user for permission to start debugging.
            task_steps (list, optional): The steps of the task to debug. Default is None.
            step_index (int, optional): The index of the step to debug. Default is None.

        Returns:
            bool: True if debugging was successful, False otherwise.
        """
        logger.info('Debugging %s', command)
        self.recursion_layer += 1
        self.agent.project.current_task.add_debugging_task(self.recursion_layer, command, user_input, issue_description)
        if self.recursion_layer > MAX_RECURSION_LAYER:
            self.recursion_layer = 0
            raise TooDeepRecursionError()

        function_uuid = str(uuid.uuid4())
        convo.save_branch(function_uuid)

        for i in range(MAX_COMMAND_DEBUG_TRIES):
            print('', type='verbose', category='agent:debugger')
            llm_response = convo.send_message('dev_ops/debug.prompt',
                {
                    'command': command['command'] if command is not None else None,
                    'user_input': user_input,
                    'issue_description': issue_description,
                    'task_steps': task_steps,
                    'step_index': step_index,
                    'os': platform.system()
                },
                DEBUG_STEPS_BREAKDOWN)

            completed_steps = []
            print_task_progress(i+1, i+1, user_input, 'debugger', 'in_progress')

            try:
                for attempt in range(MAX_COMMAND_DEBUG_TRIES):
                    steps = completed_steps + llm_response['steps']

                    result = self.agent.project.developer.execute_task(
                        convo,
                        steps,
                        test_command=command,
                        test_after_code_changes=True,
                        continue_development=False,
                        is_root_task=is_root_task,
                        continue_from_step=len(completed_steps),
                        task_source='debugger',
                    )

                    if 'step_index' in result:
                        result['os'] = platform.system()
                        step_index = result['step_index']
                        completed_steps = steps[:step_index+1]

                        convo.remove_last_x_messages(2)
                        llm_response = convo.send_message('development/task/update_task.prompt', result,
                            DEBUG_STEPS_BREAKDOWN)
                    else:
                        return result['success']

            except TokenLimitError as e:
                if self.recursion_layer > 0:
                    convo.load_branch(function_uuid)
                    self.recursion_layer -= 1
                    raise e
                else:
                    trace_code_event('token-limit-error', {'error': traceback.format_exc()})
                    convo.load_branch(function_uuid)

            except TooDeepRecursionError as e:
                convo.load_branch(function_uuid)
                raise e

            except (KeyError, IndexError) as e:
                convo.load_branch(function_uuid)
                continue

        self.recursion_layer -= 1
        return False

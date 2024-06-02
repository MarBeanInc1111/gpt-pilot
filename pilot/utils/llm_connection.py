import re
import requests
import os
import sys
import time
import json
import tiktoken
from prompt_toolkit.styles import Style
from jsonschema import validate, ValidationError
from typing import List, Dict, Any
from const.llm import MAX_GPT_MODEL_TOKENS, API_CONNECT_TIMEOUT, API_READ_TIMEOUT
from const.messages import AFFIRMATIVE_ANSWERS
from logger.logger import logger, logging
from helpers.exceptions import TokenLimitError, ApiKeyNotDefinedError, ApiError
from utils.utils import fix_json, get_prompt
from utils.function_calling import add_function_calls_to_request, FunctionCallSet, FunctionType
from utils.questionary import styled_text

import anthropic

from .telemetry import telemetry

tokenizer = tiktoken.get_encoding("cl100k_base")


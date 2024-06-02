import os

# Define constants using all capital letters for readability
MAX_GPT_MODEL_TOKENS = int(os.getenv('MAX_TOKENS', 8192))
MIN_TOKENS_FOR_GPT_RESPONSE = 600
MAX_QUESTIONS = 5
END_RESPONSE = "EVERYTHING_CLEAR"
API_CONNECT_TIMEOUT = 30  # timeout for connecting to the API and sending the request (seconds)
API_READ_TIMEOUT = 300  # timeout for receiving the response (seconds)

# Add type hints for improved code readability and tooling support
MAX_GPT_MODEL_TOKENS: int
MIN_TOKENS_FOR_GPT_RESPONSE: int
MAX_QUESTIONS: int
END_RESPONSE: str
API_CONNECT_TIMEOUT: int
API_READ_TIMEOUT: int

# Add a docstring to explain the purpose of the constants
"""
Constants used in the application.
"""

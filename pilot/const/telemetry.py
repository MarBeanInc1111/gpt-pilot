# Constants representing various thresholds for request and loop handling

"""
LARGE_REQUEST_THRESHOLD: The number of tokens that defines a large request.
SLOW_REQUEST_THRESHOLD: The number of seconds that defines a slow request.
LOOP_THRESHOLD: The number of iterations in a task that defines a loop.
"""

LARGE_REQUEST_THRESHOLD = 50000  # tokens
SLOW_REQUEST_THRESHOLD = 300  # seconds
LOOP_THRESHOLD = 3  # number of iterations in task to be considered a loop

from .utils import should_execute_step

class TestShouldExecuteStep:
    """Tests for the `should_execute_step` function."""

    def test_no_step_arg(self, should_execute_step: callable) -> None:


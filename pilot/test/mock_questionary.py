class MockQuestionary:
    """
    A mock questionary class for testing.
    """

    def __init__(self, answers: list = None, initial_state: str = 'project_description'):
        """
        Initialize the MockQuestionary object.

        :param answers: A list of strings representing the user's answers
        :param initial_state: The initial state of the questionary
        """
        if answers is None:
            answers = []
        self.answers = iter(answers)
        self.state = initial_state

    def text(self, question: str, style=None):
        """
        Print the given question and update the state accordingly.

        :param question: The question to print
        :param style: The style of the question
        :return: The MockQuestionary object
        """
        print('AI: ' + question)
        if question.startswith('User Story'):
            self.state = 'user_stories'
        elif question.endswith('write "DONE"'):
            self.state = 'DONE'
        return self

    def ask(self) -> str:
        """
        Ask the user for an answer and return it.

        :return: The user's answer
        """
        return self._ask()

    def _ask(self) -> str:
        """
        Implementation detail of the `ask` method.

        :return: The user's answer
        """
        if self.state == 'user_stories':
            answer = ''
        elif self.state == 'DONE':
            answer = 'DONE'
        else:  # if self.state == 'project_description':
            try:
                answer = next(self.answers)
            except StopIteration:
                answer = ''

        print('User:', answer)
        return answer

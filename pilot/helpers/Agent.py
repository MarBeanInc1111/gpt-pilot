class Agent:
    """Agent class representing a member of a project with a specific role."""

    def __init__(self, role: str, project: str):
        """Initialize the Agent instance with a role and a project.

        Args:
            role (str): The role of the Agent in the project.
            project (str): The name of the project the Agent is working on.

        Raises:
            ValueError: If the role or project is not a string.
        """
        if not isinstance(role, str) or not isinstance(project, str):
            raise ValueError("Role and project must be strings.")

        self.role = role
        self.project = project

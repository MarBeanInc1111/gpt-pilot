from .AbstractRole import Role, RoleStep
from . import Architect, Developer, TechLead

class Role(Role):
    ARCHITECTURE_STEP = "architecture_step"
    ENVIRONMENT_SETUP_STEP = "environment_setup_step"

class Architect(Role):
    STEPS = [
        RoleStep(ARCHITECTURE_STEP, "Define system architecture"),
        # Add more steps as needed
    ]

class Developer(Role):
    STEPS = [
        RoleStep(ENVIRONMENT_SETUP_STEP, "Set up development environment"),
        # Add more steps as needed
    ]

class TechLead(Role):
    # Define steps or other attributes as needed
    pass

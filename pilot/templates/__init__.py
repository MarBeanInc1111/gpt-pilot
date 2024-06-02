import os
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from utils.style import color_green_bold
from logger.logger import logger
from utils.exit import trace_code_event

from .node_express_mongoose import NODE_EXPRESS_MONGOOSE
from .render import Renderer

if TYPE_CHECKING:  # noqa
    from helpers.Project import Project  # noqa

PROJECT_TEMPLATES = {
    "node_express_mongoose": NODE_EXPRESS_MONGOOSE,
}


def render_and_save_files(
    template: dict,
    project_name: str,
    project_description: str,
    root_path: str,
) -> list:
    """
    Render and save files from a given template.

    :param template: the project template
    :param project_name: the name of the project
    :param project_description: the description of the project
    :param root_path: the root path of the project
    :return: a list of project files
    """
    r = Renderer(os.path.join(os.path.dirname(__file__), "tpl"))
    files = r.render_tree(template["path"], {
        "project_name": project_name,
        "project_description": project_description,
        "random_secret": str(uuid4()),
    })

    project_files = []

    for file_name, file_content in files.items():
        full_path = os.path.join(root_path, file_name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(file_content)
        except Exception as err:
            logger.error(
                f"Error saving file '{file_name}': {err}",
                exc_info=True,
            )
            continue

        rel_dir = os.path.dirname(file_name)
        project_files.append({
            "name": os.path.basename(file_name),
            "path": "/" if rel_dir in ["", "."] else rel_dir,
            "content": file_content,
        })

    return project_files


def apply_project_template(
    project: "Project",
) -> Optional[str]:
    """
    Apply a project template to a new project.

    :param project: the project object
    :return: a summary of the applied template, or None if no template was applied
    """
    template_name = project.project_template
    if not template_name or template_name not in PROJECT_TEMPLATES:
        logger.warning(f"Project template '{template_name}' not found, ignoring")
        return None

    root_path = project.root_path
    project_name = project.args['name']
    project_description = project.main_prompt
    template = PROJECT_TEMPLATES[template_name]
    install_hook = template.get("install_hook")

    project_files = render_and_save_files(template, project_name, project_description, root_path)

    print(color_green_bold(f"Applying project template {template['description']}...\n"))
    logger.info(f"Applying project template {template_name}...")

    last_development_step = project.checkpoints.get('last_development_step')
    if last_development_step:
        project.save_files_snapshot(last_development_step['id'])

    if install_hook:
        try:
            install_hook(project)
        except Exception as err:
            logger.info(
                f"Error running install hook for project template '{template_name}': {err}",
                exc_info=True,
            )

    trace_code_event('project-template', {'template': template_name})
    summary = f"The code so far includes:\n{template['summary']}"
    return summary

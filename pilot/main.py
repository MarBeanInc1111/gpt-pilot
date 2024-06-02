import os
import sys
from typing import Any, Dict, List, Union

import builtins
import json
import traceback
from dotenv import load_dotenv

# Added type hinting for function arguments and return types
def get_env_variable(variable_name: str, raise_error: bool = True) -> Union[str, None]:
    if variable_name in os.environ:
        return os.environ[variable_name]
    elif raise_error:
        raise RuntimeError(f'Missing environment variable: {variable_name}')
    else:
        return None


def init():
    load_dotenv()

    # Check if the "euclid" database exists, if not, create it
    if not database_exists():
        create_database()

    # Check if the tables exist, if not, create them
    if not tables_exist():
        create_tables()

    arguments = get_arguments()

    logger.info('Starting with args: %s', arguments)

    return arguments

# Added type hinting for function arguments and return types
def handle_telemetry(project: Any, telemetry_data: Dict[str, Any], end_result: str):
    if settings.telemetry is None:
        telemetry.setup()
        loader.save("telemetry")

    if 'app_id' in arguments:
        telemetry.set("is_continuation", True)

    if "email" in arguments:
        telemetry.set("user_contact", arguments["email"])

    if "extension_version" in arguments:
        telemetry.set("extension_version", arguments["extension_version"])

    if project is not None and project.check_ipc():
        telemetry.send()

    telemetry.record_crash(telemetry_data, end_result=end_result)

if __name__ == "__main__":
    ask_feedback = True
    project = None
    run_exit_fn = True

    args = init()

    try:
        # sys.argv.append('--ux-test=' + 'continue_development')

        builtins.print, ipc_client_instance = get_custom_print(args)

        OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY", raise_error=False)
        if '--api-key' in args:
            OPENAI_API_KEY = args['--api-key']

        OPENAI_ENDPOINT = get_env_variable("OPENAI_ENDPOINT", raise_error=False)
        if '--api-endpoint' in args:
            OPENAI_ENDPOINT = args['--api-endpoint']

        if '--get-created-apps-with-steps' in args:
            run_exit_fn = False

            if ipc_client_instance is not None:
                print({ 'db_data': get_created_apps_with_steps() }, type='info')
            else:
                print_table(get_created_apps_with_steps())

        elif '--version' in args:
            print(get_version())
            run_exit_fn = False

        elif '--ux-test' in args:
            from test.ux_tests import run_test
            run_test(args['--ux-test'], args)
            run_exit_fn = False
        else:
            handle_telemetry(project, {}, "success:exit")

            # TODO get checkpoint from database and fill the project with it
            project = Project(args, ipc_client_instance=ipc_client_instance)
            if project.check_ipc():
                handle_telemetry(project, {}, "success:exit")
                started = project.start()
                if started:
                    project.finish()
                    print('Thank you for using Pythagora!', type='ipc', category='pythagora')
                else:
                    run_exit_fn = False
                    handle_telemetry(project, {}, "failure:api-error")
                    print('Exit', type='exit')

    except (ApiError, TokenLimitError) as err:
        handle_telemetry(project, err, "failure:api-error")
        run_exit_fn = False
        if isinstance(err, TokenLimitError):
            print('', type='verbose', category='error')
            print(color_red(
                "We sent too large request to the LLM, resulting in an error. "
                "This is usually caused by including framework files in an LLM request. "
                "Here's how you can get GPT Pilot to ignore those extra files: "
                "https://bit.ly/faq-token-limit-error"
            ))
        print('Exit', type='exit')

    except KeyboardInterrupt:
        handle_telemetry(project, {}, "interrupt")
        if project is not None and project.check_ipc():
            handle_telemetry(project, {}, "interrupt")
            run_exit_fn = False

    except GracefulExit:
        # can't call project.finish_loading() here because project can be None
        run_exit_fn = False
        print('', type='loadingFinished')
        print('Exit', type='exit')

    except Exception as err:
        print('', type='verbose', category='error')
        print(color_red('---------- GPT PILOT EXITING WITH ERROR ----------'))
        traceback.print_exc()
        print(color_red('--------------------------------------------------'))
        ask_feedback = False
        handle_telemetry(project, err, "failure:unknown")

    finally:
        if project is not None:
            if project.check_ipc():
                ask_feedback = False
            project.current_task.exit()
            project.finish_loading(do_cleanup=False)
        if run_exit_fn:
            exit_gpt_pilot(project, ask_feedback)

# Added a new function to print the table
def print_table(data: List[Dict[str, Any]]):
    print('----------------------------------------------------------------------------------------')
    print('app_id                                step                 dev_step  name')
    print('----------------------------------------------------------------------------------------')
    for app in data:
        print(f"{app['id']}: {app['status']:20}      "
              f"{'' if len(app['development_steps']) == 0 else app['development_steps'][-1]['id']:3}"
              f"  {app['name']}")

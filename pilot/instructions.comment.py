# Init CLI
def init_cli():
    # 1. Show the type of the app that needs to be created
    print("1. Choose the type of the app that needs to be created:")
    app_type = input("Enter the app type or press enter for the default type: ").strip()
    if not app_type:
        app_type = "default"

    # 1.c Check if the wanted app can be created
    if app_type not in ["web", "mobile", "default"]:
        print(f"Error: The app type '{app_type}' cannot be created.")
        exit()
    print(f"Confirmation: The app type '{app_type}' will be created.")

    # 2. Ask user for the main definition of the app
    app_definition = input("2. Enter the main definition of the app: ").strip()

    # Start the processing queue
    # ...

# Show the user flow of the app
def show_user_flow(app_type):
    # 2.c Ask user to press enter if it's ok, or to add the user flow they want
    print(f"3. Enter the user flow for the {app_type} app:")
    user_flow = input("Enter the user flow or press enter for the default flow: ").strip()
    if not user_flow:
        user_flow = "default"

    # Ask for input until they just press enter
    # Recompute the user flow and ask again
    # ...

# Show the components of the app
def show_components(app_type):
    # 3.1 Frontend
    print(f"4. Enter the frontend components for the {app_type} app:")
    frontend_components = input("Enter the frontend components or press enter for the default components: ").strip()
    if not frontend_components:
        frontend_components = "default"

    # 3.2 Backend
    print(f"5. Enter the backend components for the {app_type} app:")
    backend_components = input("Enter the backend components or press enter for the default components: ").strip()
    if not backend_components:
        backend_components = "default"

    # 3.3 Database
    print(f"6. Enter the database components for the {app_type} app:")
    database_components = input("Enter the database components or press enter for the default components: ").strip()
    if not database_components:
        database_components = "default"

    # 3.4 Config
    print(f"7. Enter the config components for the {app_type} app:")
    config_components = input("Enter the config components or press enter for the default components: ").strip()
    if not config_components:
        config_components = "default"

    # 3.x Ask user to press enter if it's ok, or to add the components they want
    # Ask for input until they just press enter
    # Recompute the components and ask again
    # ...

# Break down the files that need to be created to support each of the components
def break_down_files(app_type, components):
    # Ask user to press enter if it's ok, or to add the files they want
    # Ask for input until they just press enter
    # Recompute the files and ask again
    # ...

# Break down the tests that need to be created
def break_down_tests(app_type, files, functions):
    # In the prompt, send all the files and functions
    # Start from the high level tests and go down to the unit tests
    # 6.1 Ask user to press enter if it's ok, or to add the tests they want
    # Ask for input until they just press enter
    # Recompute the tests and ask again
    # ...

# Write the tests
def write_tests(app_type, tests):
    # ...

# Write the files for each test
def write_test_files(app_type, test_files):
    # ...

# Run each created test once the code is written
def run_tests(app_type, tests, test_files):
    # ...

# Try debugging 5 times
def try_debugging(app_type, files, functions, tests, test_files):
    # ...

# Create build/run script
def create_build_run_script(app_type, files, functions, tests, test_files):
    # ...

# Run the app
def run_app(app_type, files, functions):
    # ...

# 4. Show the components of the app setup
def show_app_setup(app_type):
    # a. Installation process
    print(f"{app_type} app installation process:")
    # ...

    # b. Configuration process
    print(f"{app_type} app configuration process:")
    # ...

    # c. Running process
    print(f"{app_type} app running process:")
    # ...

    # d. Building process
    print(f"{app_type} app building process:")
    # ...

    # e. Testing process
    print(f"{app_type} app testing process:")
    # ...

# Init CLI
init_cli()

# Show the user flow of the app
show_user_flow("web")

# Show the components of the app
components = show_components("web")

# Break down the files that need to be created to support each of the components
files = break_down_files("web", components)

# Break down the tests that need to be created
tests = break_down_tests("web", files, functions)

# Write the tests
write_tests("web", tests)

# Write the files for each test
write_test_files("web", test_files)

# Run each created test once the code is written
run_tests("web", tests, test_files)

# Try debugging 5 times
try_debugging("web", files, functions, tests, test_files)

# Create build/run script
create_build_run_script("web", files, functions, tests, test_files)

# Run the app
run_app("web", files, functions)

# Show the components of the app setup
show_app_setup("web")

from uuid import UUID
from context import text_studio
from project import Project

USER_PROMPT = "Please enter a command to run (q - quit, h - help): "


def get_user_input():
    command = input(USER_PROMPT).strip().lower()
    return parse_command(command)


def parse_command(command):
    split_data = command.split()
    command = command
    arg = ""
    if len(split_data) > 1:
        command = split_data[0]
        arg = split_data[1]
    return command, arg


def print_help():
    print(
        "Commands:\n"
        + "help (h)\t\t\tShow help.\n"
        + "project (p) <file path>\t\tCreate a project or open the project at the specified file path.\n"
        + "run (r) <id>\t\t\tRun the project module or pipeline with the specified ID.\n"
        + "save (s) <file path>\t\tSave a project to its current file or the provided file path.\n"
        + "quit (q)\t\t\tQuit the application."
    )


if __name__ == "__main__":
    command, arg = get_user_input()
    project = None
    while command != "quit" and command != "q":
        if command == "help" or command == "h":
            print_help()
        elif command == "project" or command == "p":
            if arg:
                print("Loading project...")
                project = Project(filepath=arg)
            else:
                print("Creating new project...")
                author = input(
                    "Please provide the name of the project owner: "
                )
                project = Project(author=author)
            print(project)
        elif command == "run" or command == "r":
            if project:
                module_id = None
                try:
                    module_id = UUID(arg)
                except ValueError:
                    print(
                        "Please provide a valid ID (hexadecimal UUID string)."
                    )

                if module_id:
                    input_id = input("Please provide the input dataset ID: ")
                    input_id = "5eacbf07-d9b8-4d02-b674-8badb7703e2a"
                    id = None
                    try:
                        id = UUID(input_id)
                    except ValueError:
                        print(
                            "Please provide a valid dataset ID (hexadecimal UUID string)."
                        )

                    if id:
                        output_path = input(
                            "Please provide the output dataset path: "
                        ).strip()

                        try:
                            print("Running module...")
                            project.run(
                                module_id, id, output_path, verbose=True
                            )
                            print("Execution complete...")
                        except KeyError as e:
                            print("Unsuccessful execution: {}".format(e))
            else:
                print(
                    "Cannot execute modules until a project is loaded. Please load or create a project."
                )

        elif command == "save":
            print("Saving project...")
            project.save()
        else:
            print('"{}" is not a supported command.'.format(command))
        command, arg = get_user_input()

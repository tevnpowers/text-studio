import argparse

from context import text_studio
from project import Project


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some text.")

    parser.add_argument(
        "--project",
        metavar="P",
        type=str,
        nargs=1,
        help="A text studio project file (json)",
    )

    parser.add_argument(
        "--loader", metavar="L", type=str, nargs=1, help="A data loader ID"
    )

    parser.add_argument(
        "--data", metavar="D", type=str, nargs=1, help="File path to the data to load"
    )

    args = parser.parse_args()
    if args.project:
        print("Loading project...")
        project = Project(args.project[0])

        print("Running FanFict pipeline...")
        project.run_pipeline("FanFict", "../data/story_content.csv")
    else:
        print("*" * 21)
        print("*CLI for Text Studio*")
        print("*" * 21)
        print("\n")
        print(parser.description)
        parser.print_usage()
        print("\n")

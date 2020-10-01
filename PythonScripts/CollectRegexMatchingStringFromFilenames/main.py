from pathlib import Path
import re
from typing import Union


default_input_dir = Path(__file__).parent.absolute() / "input_dir"
default_output_dir = Path(__file__).parent.absolute() / "output_dir"
default_regex = r"_([^_]*)\."


def extractRegexMatchingStrings(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    regex: str = default_regex,
):
    if isinstance(input_dir, str):
        input_dir = Path(input_dir)
    if isinstance(output_dir, str):
        input_dir = Path(output_dir)

    # Check if input directory exists, raise exception otherwise
    if not input_dir.is_dir():
        import errno
        import os

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(input_dir))

    # Create output directory if not exists
    output_dir.mkdir(exist_ok=True)

    # Find file types present in input directory
    file_types = set(map(lambda x: x.suffix, input_dir.glob("*")))

    # Process each file type
    for file_type in file_types:
        # Create <file_type>_files.csv file e.g. pdf_files.csv
        output_file = output_dir / "{}_files.csv".format(str(file_type).lstrip("."))
        # Create output file if not exists
        output_file.touch(exist_ok=True)
        # list of all files name of file_type
        file_names = map(lambda x: x.name, input_dir.glob("*{}".format(file_type)))
        # process each file
        for file_name in file_names:
            # Append regex matching strings extracted from file name
            output_file.open("a").write((" ".join(re.findall(regex, file_name))) + "\n")


if __name__ == "__main__":
    import argparse

    def is_valid_dir(path: Union[str, Path]):
        path = Path(path) if isinstance(path, str) else path
        if not path.exists():
            raise argparse.ArgumentTypeError(f"{path} is not a valid path")

        if not path.is_dir():
            raise argparse.ArgumentTypeError(f"{path} is not a valid path")

        return path

    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-re",
        "--regex",
        help=f'regex to search in filenames. Default is "{default_regex}"',
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        help="directory containing input files",
        type=is_valid_dir,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="directory to store output files",
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    input_dir = Path(input_dir).absolute() if input_dir else default_input_dir
    output_dir = Path(output_dir).absolute() if output_dir else default_output_dir

    regex = args.regex or default_regex

    extractRegexMatchingStrings(input_dir, output_dir, regex)

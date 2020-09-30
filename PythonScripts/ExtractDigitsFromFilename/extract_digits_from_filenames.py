from pathlib import Path
import re

# Change this to absolute path of input directory
input_dir = Path(__file__).parent.absolute() / "input_dir"
# Change this to absolute path of output directory
output_dir = Path(__file__).parent.absolute() / "output_dir"

# Check if input directory exists, return otherwise
if not input_dir.exists():
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
    file_names = map(
        lambda x: x.with_suffix("").name, input_dir.glob("*{}".format(file_type))
    )
    # process each file
    for file_name in file_names:
        # Append digits extracted from file name
        output_file.open("a").write((" ".join(re.findall(r"\d+", file_name))) + "\n")
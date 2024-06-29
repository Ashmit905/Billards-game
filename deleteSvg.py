import os
def delete_svg_files():
    # Get the current directory
    directory = os.getcwd()

    # Define the pattern for files to be deleted
    pattern = "table*.svg"

    # Use list comprehension to find files matching the pattern
    matching_files = [file for file in os.listdir(directory) if file.startswith("table") and file.endswith(".svg")]

    # Iterate over matching files and delete them
    for file in matching_files:
        os.remove(os.path.join(directory, file))
        print(f"Deleted file: {file}")

if __name__ == "__main__":
    delete_svg_files()


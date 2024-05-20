import os
import shutil
import subprocess
from typing import Tuple, Dict

docs_dir = f'{os.getcwd()}/docs'

def git_clone_fedora_documentation() -> None:
    """
    Clones the Fedora documentation repository and removes unused packages.
    """
    rurl = "https://pagure.io/fedora-docs/quick-docs.git"

    os.makedirs(docs_dir, exist_ok=True)
    os.chdir(docs_dir)

    subprocess.run(["git", "clone", rurl])
    subprocess.run(["git", "clone", rurl])

    shutil.copytree("quick-docs/modules/ROOT/pages", ".", dirs_exist_ok=True)
    shutil.rmtree("quick-docs")


def split_single_doc(input_file: str) -> None:
    """
    The function creates a category folder corresponding to the category of the given file, 
    a folder for the given file in which it creates a separate file for each header
    and Index.adoc, which contains metadata and a general description of the problem
    """
    directory, filename = os.path.split(input_file)
    filename_without_extension = os.path.splitext(filename)[0]
    directory_name = filename_without_extension.split("-")[0]
    
    output_directory = os.path.join(directory, directory_name)
    os.makedirs(output_directory, exist_ok=True)
    
    nested_directory = os.path.join(output_directory, filename_without_extension)
    os.makedirs(nested_directory, exist_ok=True)
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    sections = {}
    current_section = ""
    
    for line in lines:
        if line.startswith('=') and not line.startswith('==='):
            if line.startswith('=='):
                current_section = line.strip()[2:].strip()
            else:
                current_section = line.strip()[1:].strip()
            sections[current_section] = f"{current_section}\n"
        elif current_section:
            sections[current_section] += line
    
    index_content = ""
    mapping_table = str.maketrans({"/": "_", " ": "-"})
    for section, content in sections.items():
        if section == list(sections.keys())[0]:
            index_content = content
            continue
        file_name = section.translate(mapping_table) + ".adoc"
        file_path = os.path.join(nested_directory, file_name)
        with open(file_path, 'w') as f:
            f.write(content)
    
    index_file_path = os.path.join(nested_directory, "Index.adoc")
    with open(index_file_path, 'w') as f:
        f.write(index_content)


def reorganize_clone_repo() -> None:
    """
    Transforms any .adoc file with the help of the function split_single_doc
    """
    for filename in os.listdir(docs_dir):
        if filename.endswith(".adoc"):
            input_file = os.path.join(docs_dir, filename)
            split_single_doc(input_file)
            os.remove(input_file)


def get_file_tree_diagram() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Return files dicts.
    First is category to categories problem list.
    Second is problem to headers list.
    """
    dir_dict = {}
    adoc_dict = {}

    for root, dirs, files in os.walk(docs_dir):
        if dirs:
            dir_dict[os.path.basename(root)] = dirs
        if files:
            adoc_dict[os.path.basename(root)] = [os.path.splitext(file)[0] for file in files if file.endswith(".adoc")]


    return dir_dict, adoc_dict

def prepare_data() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Prepares fedora documentation for appropriate form
    """
    if os.path.exists(docs_dir):
        return get_file_tree_diagram()
    git_clone_fedora_documentation()
    reorganize_clone_repo()

    return get_file_tree_diagram()
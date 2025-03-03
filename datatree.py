"""This is the main file of the project. It will be used to run the project.
"""

import os
import json
import shutil
from typing import List, Dict

def create_config(project_name: str) -> None:
    """This function will create a new config file for the project.

    Args:
        project_name (str): The name of the project.
    """

    accepted_image_formats = ["jpg", "jpeg", "png", "gif"]

    # create the config file
    config: Dict[str, str | List[str]] = {
        "project_name": project_name,
        "accepted_image_formats": accepted_image_formats,
        "project_root": "1"
    }

    with open(f"{project_name}/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def create_project(project_name: str) -> None:
    """This function will create a new project with the given name.

    Args:
        project_name (str): The name of the project.
    """

    # create the project directory
    os.makedirs(project_name, exist_ok=True)

    # create the config file
    create_config(project_name)

    # create the sections directory
    os.makedirs(f"{project_name}/sections", exist_ok=True)

    # create the images directory
    os.makedirs(f"{project_name}/images", exist_ok=True)

    # add a base empty section
    create_section(project_name)

def get_free_section_id(project_name: str) -> str:
    """This function will return a free section id for the project.

    Args:
        project_name (str): The name of the project.

    Returns:
        str: The free section id.
    """

    section_ids = os.listdir(f"{project_name}/sections")

    for i in range(1, len(section_ids) + 2):
        if str(i) not in section_ids:
            return str(i)

def get_free_image_id(project_name: str) -> str:
    """This function will return a free image id for the project.

    Args:
        project_name (str): The name of the project.

    Returns:
        str: The free image id.
    """

    image_ids = os.listdir(f"{project_name}/images")

    for i in range(1, len(image_ids) + 2):
        if str(i) not in image_ids:
            return str(i)

def create_section(project_name: str) -> str:
    """This function will add a new section to the project.

    Args:
        project_name (str): The name of the project.
    
    Returns:
        str: The id of the section.
    """

    section_id = get_free_section_id(project_name)

    # create the section directory
    os.makedirs(f"{project_name}/sections/{section_id}", exist_ok=True)

    # create the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    # create the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    # create the text file
    with open(f"{project_name}/sections/{section_id}/text.txt", "w", encoding="utf-8") as f:
        f.write("")

    return section_id

def delete_section(project_name: str, section_id: str) -> None:
    """This function will delete a section from the project.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
    """

    # delete the section directory
    if os.path.exists(f"{project_name}/sections/{section_id}"):
        shutil.rmtree(f"{project_name}/sections/{section_id}")
    else:
        print("Section does not exist.")

def add_image(project_name: str, image_path: str) -> None:
    """This function will add an image to the project.

    Args:
        project_name (str): The name of the project.
        image_path (str): The path of the image.
    """

    image_id = get_free_image_id(project_name)

    # get the image format
    image_format = image_path.split(".")[-1]

    # read the config file
    config = read_config(project_name)

    # check if the image format is accepted
    if image_format in config["accepted_image_formats"]:
        # copy the image to the images directory
        shutil.copy(image_path, os.path.join(project_name, "images", f"{image_id}.{image_format}"))
    else:
        print("Image format not accepted.")

def add_link_to_section(project_name: str, section_id: str, section_linked_id: str) -> None:
    """This function will add a link to a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        section_linked_id (str): The id of the link.
    """

    if section_id == section_linked_id:
        print("Can't link a section to itself.")
        return

    # read the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    # add the link to the links json file
    if section_linked_id not in links:
        links.append(section_linked_id)

    with open(f"{project_name}/sections/{section_id}/links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4)

def add_image_to_section(project_name: str, section_id: str, image_id: str) -> None:
    """This function will add an image to a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        image_id (str): The id of the image.
    """

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # add the image to the images json file
    if image_id not in images:
        images.append(image_id)

    with open(f"{project_name}/sections/{section_id}/images.json", "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4)

def remove_link_from_section(project_name: str, section_id: str, section_linked_id: str) -> None:
    """This function will remove a link from a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        section_linked_id (str): The id of the link.
    """

    # read the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    # remove the link from the links json file
    if section_linked_id in links:
        links.remove(section_linked_id)

    with open(f"{project_name}/sections/{section_id}/links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4)

def remove_image_from_section(project_name: str, section_id: str, image_id: str) -> None:
    """This function will remove an image from a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        image_id (str): The id of the image.
    """

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # remove the image from the images json file
    if image_id in images:
        images.remove(image_id)

    with open(f"{project_name}/sections/{section_id}/images.json", "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4)

def set_text_to_section(project_name: str, section_id: str, text: str = "") -> None:
    """This function will set the text of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        text (str, optional): The text to set. Defaults to
        an empty string.
    """

    # write the text to the text file
    with open(f"{project_name}/sections/{section_id}/text.txt", "w", encoding="utf-8") as f:
        f.write(text)

def get_text_from_section(project_name: str, section_id: str) -> str:
    """This function will return the text of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.

    Returns:
        str: The text of the section.
    """

    # read the text file
    with open(f"{project_name}/sections/{section_id}/text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    return text

def get_links_from_section(project_name: str, section_id: str) -> List[str]:
    """This function will return the links of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.

    Returns:
        list: The links of the section.
    """

    # read the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    return links

def get_images_from_section(project_name: str, section_id: str) -> List[str]:
    """This function will return the images of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
    
    Returns:
        list: The images ids of the section
    """

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    return images

def get_image_path(project_name: str, image_id: str) -> str|None:
    """This function will return the path of an image.

    Args:
        project_name (str): The name of the project.
        image_id (str): The id of the image.

    Returns:
        str: The path of the image. None if the image does not exist.
    """

    image_name = None

    all_images = os.listdir(f"{project_name}/images")
    for image in all_images:
        if image.split(".")[0] == image_id:
            image_name = image
            break

    image_path = os.path.join(project_name, "images",
                              image_name) if image_name else None

    return image_path

def list_sections(project_name: str) -> List[str]:
    """This function will return the list of sections in the project.

    Args:
        project_name (str): The name of the project.

    Returns:
        list: The list of sections.
    """

    sections = os.listdir(f"{project_name}/sections")

    return sections

def read_config(project_name: str) -> Dict[str, str | List[str]]:
    """This function will read the config file of the project.

    Args:
        project_name (str): The name of the project.

    Returns:
        dict: The config of the project.
    """

    with open(f"{project_name}/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    return config

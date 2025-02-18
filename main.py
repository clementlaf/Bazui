"""This is the main file of the project. It will be used to run the project.
"""

import os
import json
import shutil

def create_config(project_name):
    """This function will create a new config file for the project.

    Args:
        project_name (str): The name of the project.
    """

    print(f"Creating config file for project: {project_name}")

    accepted_image_formats = ["jpg", "jpeg", "png", "gif"]

    # create the config file
    config = {
        "project_name": project_name,
        "accepted_image_formats": accepted_image_formats,
        "project_root": "1"
    }

    with open(f"{project_name}/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print("Config file created successfully.")

def create_project(project_name):
    """This function will create a new project with the given name.

    Args:
        project_name (str): The name of the project.
    """

    print(f"Creating project: {project_name}")

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

    print("Project created successfully.")

def get_free_section_id(project_name):
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

def get_free_image_id(project_name):
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

def create_section(project_name):
    """This function will add a new section to the project.

    Args:
        project_name (str): The name of the project.
        section_name (str): The name of the section.
    """

    section_id = get_free_section_id(project_name)
    print(f"Adding section: {section_id}")

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

    print("Section added successfully.")

def delete_section(project_name, section_id):
    """This function will delete a section from the project.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
    """

    print(f"Deleting section: {section_id}")

    # delete the section directory
    if os.path.exists(f"{project_name}/sections/{section_id}"):
        os.rmdir(f"{project_name}/sections/{section_id}")
    else:
        print("Section does not exist.")

    print("Section deleted successfully.")

def delete_link(project_name, link_id):
    """This function will delete a link from the project.

    Args:
        project_name (str): The name of the project.
        link_id (str): The id of the link.
    """

    print(f"Deleting link: {link_id}")

    # delete the link directory
    if os.path.exists(f"{project_name}/links/{link_id}"):
        os.rmdir(f"{project_name}/links/{link_id}")
    else:
        print("Link does not exist.")

    print("Link deleted successfully.")

def add_image(project_name, image_path):
    """This function will add an image to the project.

    Args:
        project_name (str): The name of the project.
        image_path (str): The path of the image.
    """

    print(f"Adding image: {image_path}")
    image_id = get_free_image_id(project_name)

    # get the image format
    image_format = image_path.split(".")[-1]

    # read the config file
    with open(f"{project_name}/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # check if the image format is accepted
    if image_format in config["accepted_image_formats"]:
        # copy the image to the images directory
        shutil.copy(image_path, os.path.join(project_name, "images", f"{image_id}.{image_format}"))
    else:
        print("Image format not accepted.")

    print("Image added successfully.")

def add_link_to_section(project_name, section_id, section_linked_id):
    """This function will add a link to a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        section_linked_id (str): The id of the link.
    """

    print(f"Adding link: {section_linked_id} to section: {section_id}")

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

    print("Link added successfully.")

def add_image_to_section(project_name, section_id, image_id):
    """This function will add an image to a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        image_id (str): The id of the image.
    """

    print(f"Adding image: {image_id} to section: {section_id}")

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # add the image to the images json file
    if image_id not in images:
        images.append(image_id)

    with open(f"{project_name}/sections/{section_id}/images.json", "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4)

    print("Image added successfully.")

def remove_link_from_section(project_name, section_id, section_linked_id):
    """This function will remove a link from a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        section_linked_id (str): The id of the link.
    """

    print(f"Removing link: {section_linked_id} from section: {section_id}")

    # read the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    # remove the link from the links json file
    if section_linked_id in links:
        links.remove(section_linked_id)

    with open(f"{project_name}/sections/{section_id}/links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4)

    print("Link removed successfully.")

def remove_image_from_section(project_name, section_id, image_id):
    """This function will remove an image from a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        image_id (str): The id of the image.
    """

    print(f"Removing image: {image_id} from section: {section_id}")

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # remove the image from the images json file
    if image_id in images:
        images.remove(image_id)

    with open(f"{project_name}/sections/{section_id}/images.json", "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4)

    print("Image removed successfully.")

def set_text_to_section(project_name, section_id, text=""):
    """This function will set the text of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
        text (str, optional): The text to set. Defaults to
        an empty string.
    """

    print(f"Setting text to section: {section_id}")

    # write the text to the text file
    with open(f"{project_name}/sections/{section_id}/text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Text set successfully.")

def get_text_from_section(project_name, section_id):
    """This function will return the text of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.

    Returns:
        str: The text of the section.
    """

    print(f"Getting text from section: {section_id}")

    # read the text file
    with open(f"{project_name}/sections/{section_id}/text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print("Text got successfully.")

    return text

def get_links_from_section(project_name, section_id):
    """This function will return the links of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.

    Returns:
        list: The links of the section.
    """

    print(f"Getting links from section: {section_id}")

    # read the links json file
    with open(f"{project_name}/sections/{section_id}/links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    print("Links got successfully.")

    return links

def get_images_from_section(project_name, section_id):
    """This function will return the images of a section.

    Args:
        project_name (str): The name of the project.
        section_id (str): The id of the section.
    """

    print(f"Getting images from section: {section_id}")

    # read the images json file
    with open(f"{project_name}/sections/{section_id}/images.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    print("Images got successfully.")

    return images

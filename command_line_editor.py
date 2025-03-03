"""This simple commande line editor is a simple interface to interact with the main module.
 It allows the user to create, open, and edit projects.
 It is mainly used for testing purposes.
"""

import datatree
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def help():
    print("Help: This is a command line editor")
    print("Commands:")
    print("exit: Quit the editor")
    print("help: Show this help message")
    print("open _project_path: Open a project")
    print("close: Close the current project")
    print("create _project_name: Create a new project")
    print("move _section_name: Move to a section")
    print("print: Print the current section's links, images, and text")
    print("add link _link: Add a link to the current section")
    print("add image _image: Add an image to the current section")
    print("add text _text: Add text to the current section")
    print("add section: Add a new section")
    print("remove link _link: Remove a link from the current section")
    print("remove image _image: Remove an image from the current section")
    print("remove section _section_name: Remove a section")
    print("list: List all sections in the current project")


def interface():
    print("My Command Line Editor")

    project_opened = None
    current_section = "1"
    help()

    while True:

        input_message = "Enter a command: "
        if project_opened is not None:
            input_message = f"{project_opened}> "
            if current_section is not None:
                input_message = f"{project_opened}/{current_section}> "
        command = input(input_message)
        clear_console()
        print(f"Command entered: {command}")
        if command == 'exit':
            break
        elif command == 'help':
            help()
        elif command.startswith('open '):
            project_path = command.split(' ')[1]
            print(f"Opening project: {project_path}")
            project_opened = project_path
        elif command == 'close':
            print(f"Closing project: {project_opened}")
            project_opened = None
        elif command.startswith('create '):
            project_name = command.split(' ')[1]
            project_opened = project_name
            current_section = "1"
            print(f"Creating project: {project_name}")
            datatree.create_project(project_name)
        elif command.startswith('move '):
            section_name = command.split(' ')[1]
            print(f"Moving to section: {section_name}")
            current_section = section_name
        elif command == "print":
            section_links = datatree.get_links_from_section(project_opened, current_section)
            section_images = datatree.get_images_from_section(project_opened, current_section)
            section_text = datatree.get_text_from_section(project_opened, current_section)
            print(f"Links: {section_links}")
            print(f"Images: {section_images}")
            print(f"Text: {section_text}")
        elif command.startswith('add '):
            add_type = command.split(' ')[1]
            if add_type == 'link':
                add_value = command.split(' ')[2]
                datatree.add_link_to_section(project_opened, current_section, add_value)
            elif add_type == 'image':
                add_value = command.split(' ')[2]
                datatree.add_image_to_section(project_opened, current_section, add_value)
            elif add_type == 'text':
                add_value = command.split(' ')[2]
                datatree.set_text_to_section(project_opened, current_section, add_value)
            elif add_type == 'section':
                datatree.create_section(project_opened)
        elif command.startswith('remove '):
            remove_type = command.split(' ')[1]
            if remove_type == 'link':
                remove_value = command.split(' ')[2]
                datatree.remove_link_from_section(project_opened, current_section, remove_value)
            elif remove_type == 'image':
                remove_value = command.split(' ')[2]
                datatree.remove_image_from_section(project_opened, current_section, remove_value)
            elif remove_type == 'section':
                remove_value = command.split(' ')[2]
                datatree.delete_section(project_opened, remove_value)
        elif command == "list":
            sections = datatree.list_sections(project_opened)
            print(f"Sections: {sections}")
        else:
            print(f"You entered: {command}")

if __name__ == '__main__':
    interface()

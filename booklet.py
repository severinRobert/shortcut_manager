from json import loads, dumps
from os import remove, path


def write(filename, content, writing_type="w"):
    file = open(filename, writing_type)
    file.write(content)
    file.close()


class Booklet:
    """
    initialise the booklet with the content of the data.txt
    """

    def __init__(self):
        self.booklet = loads(open("data.txt", "r").read())

    """
    adding a shortcut to the booklet
    name : name of the shortcut
    links : list of all links for the shortcut
    program : program which be used by the shortcut to open links
    """

    def add(self, name, links, program):
        if program == "":
            program = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.booklet.update({name: {"links": links, "program": program}})
        write("data.txt", dumps(self.booklet))
        print(f"{name} added to the booklet")

    """
    shows information about the booklet
    name :  if not mentioned it shows all name of shortcuts
            elif name is in the booklet it shows name, links and program of the selected shortcut
            else say that the name isn't  in the booklet
    """

    def show(self, name=""):
        if name == "":
            for i in self.booklet:
                print(f"name : {i}")
        elif name in self.booklet:
            print(f"name : {name}")
            print("links :")
            ctr = 0;
            for i in self.booklet[name]["links"]:
                print(f"    {ctr} : {i}")
                ctr+=1;
            print(f"program : {self.booklet[name]['program']}")
        else:
            print(f"{name} is not in the booklet, command 'show' to see all shortcuts")

    """
    delete the selected shortcut
    name : name of the shortcut to delete 
            if it doesn't match with any shortcut in the booklet we simply say it to user
    """

    def delete(self, name):
        if name in self.booklet:
            del self.booklet[name]
            write("data.txt", dumps(self.booklet))
            print(f"'{name}' has been deleted")
        else:
            print(f"'{name}' is not in the booklet")

    """
    create a file for the shortcut selected
    name : name of the shortcut make in file
            if it doesn't match with any shortcut in the booklet we simply say it to user
    """

    def create(self, name):
        if name in self.booklet:
            content = f"""
import os
import webbrowser

links = {self.booklet[name]["links"]}
program_path = '{self.booklet[name]["program"]}'
os.startfile(program_path)
for link in links:
    webbrowser.open(link)
"""
            write(f"shortcuts/{name}.py", content)
            print(f"the shortcut '{name}' has been created")
        else:
            print(f"{name} is not in the booklet")

    def copy(self, name_to_copy, new_name):
        self.booklet[new_name] = self.booklet[name_to_copy]

    """
    modify a name, a link, a program or add a link
    name : name of the shortcut to modify
    element : name/link/program
    link_number : if link, index of the link to modify
    option : if link, replace or delete the link selected
    """

    def alter(self, name, element, link_number=0, option=""):
        if "l" in element:
            if "r" in option:
                new_value = input("Choose the new value of the link : ")
                length_links = len(self.booklet[name]["links"])

                # link_number has to be between 0 include and length of list not include
                if length_links > link_number >= 0:
                    self.booklet[name]["links"][link_number] = new_value
                    if path.exists(f"shortcuts/{name}.py"):
                        remove(f"shortcuts/{name}.py")
                        self.create(name)
                    print(f"the link has been changed to {new_value}")

                # or we add the new_value at the end of the list
                else:
                    self.booklet[name]["links"].append(new_value)
                    if path.exists(f"shortcuts/{name}.py"):
                        remove(f"shortcuts/{name}.py")
                        self.create(name)
                    print(f"{new_value} has been added to links of {name}")

            elif "d" in option:
                link = self.booklet[name]["links"][link_number]
                self.booklet[name]["links"].pop(link_number)
                if path.exists(f"shortcuts/{name}.py"):
                    remove(f"shortcuts/{name}.py")
                    self.create(name)
                print(f"{link} has been deleted of the links list of {name}")
            else:
                print(f"option {option} is not found")
        elif "p" in element or "n" in element:
            new_value = input(f"Choose the new value of {element} : ")
            if "p" in element:
                self.booklet[name]["program"] = new_value
                if path.exists(f"shortcuts/{name}.py"):
                    remove(f"shortcuts/{name}.py")
                    self.create(name)
            elif "n" in element:
                if " " in new_value:
                    print(f"'{new_value}' is invalid name, name can not have spaces")
                else:
                    self.booklet[new_value] = self.booklet.pop(name)
                    if path.exists(f"shortcuts/{name}.py"):
                        remove(f"shortcuts/{name}.py")
                        self.create(name)
        else:
            print(f"option {element} is not found")
        write("data.txt", dumps(self.booklet))

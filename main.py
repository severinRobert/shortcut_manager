from booklet import Booklet
from os import remove, path, system


def exec_file(filename):
    system(f"python3 shortcuts/{filename}.py")


if __name__ == "__main__":
    # initialize instance of Booklet
    book = Booklet()
    print("Hi, welcome to the shortcut manager \nhelp to see the possible commands.")

    while True:
        command = input("    >>>")
        command = command.split(' ')

    # cleaning the command in case of several space
        others = False
        ctr, word = 0, 0
        for i in range(len(command)):
            if command[ctr] == "" or others:
                command.pop(ctr)
                if word > 0:
                    others = True
                ctr -= 1
            else:
                word += 1
            ctr += 1

    # start
        if len(command) == 0:
            pass
        elif command[0] == "show" or command[0] == "sh":
            name = ""
            if len(command) == 2:
                name = command[1]
            book.show(name)

        elif command[0] == "help":
            print("""command   |   [option]   |   description
- - - - - - - - - - - - - - - - - - - - - -
add             add a shortcut to the booklet
alter           modify a shortcut and file / add a new link
    [name]          select the shortcut to modify
    [element]       element to modify name/link/program
    [index]         index of the link to modify
    [option]        delete or replace the link
copy            copy a shortcut
build           build a file with the designated shortcut
delete [element]    delete the designated shortcut/file
exit            exit the manager
help            this help menu
open [name]         execute the shortcut's file
show            show all the shortcut's name
    [name]          show the details about the shortcut""")

        elif command[0] == "add":
            name = input("name of the shortcut : ") if len(command) == 1 else command[1]
            links = []
            while True:
                link = input('link for the shortcut (tap "ok" to stop) : ')
                if link == "ok":
                    break
                links.append(link)
            program = input('web browser path or pass for default : ')
            book.add(name, links, program)

        elif command[0] == "copy" or command[0] == "cop":
            name_to_copy = input("name of the shortcut to copy : ") if len(command) < 2 else command[1]
            if name_to_copy not in book.booklet:
                print(f"'{name_to_copy}' is not in the booklet")
            else:
                new_name = input("name of the new shortcut : ") if len(command) < 3 else command[2]
                if " " in new_name:
                    print(f"'{new_name}' is invalid name cause of spaces")
                else:
                    book.copy(name_to_copy, new_name)

        elif command[0] == "delete" or command[0] == "del":
            element = input("shortcut/file : ") if len(command) < 2 else command[1]
            name = input("name of the shortcut : ") if len(command) < 3 else command[2]
            if "s" in element:
                book.delete(name)
            elif "f" in element:
                remove(f"shortcuts/{name}.py")
                print(f"file {name} deleted")
            else:
                print(f"{element} is not available")
        elif command[0] == "build":
            name = input("name of the shortcut : ") if len(command) == 1 else command[1]
            book.create(name)

        elif command[0] == "alter":
            name = input("name of the shortcut : ") if len(command) == 1 else command[1]
            if name in book.booklet:
                element = input("what do you want to change(name/link/program) : ") if len(command) < 3 else command[2]
                if "l" in element:
                    length_links = len(book.booklet[name]["links"])
                    if len(command) < 4:
                        for i in range(length_links):
                            print(f"{i} : {book.booklet[name]['links'][i]}")
                        print(f"{length_links} : new link")
                        link_number = input("number of the link : ")
                    else:
                        link_number = command[3]
                    link_number = int(link_number)

                    if link_number < length_links:
                        option = input("delete or replace : ") if len(command) < 5 else command[4]
                    else:
                        option = "replace"
                    book.alter(name, element, link_number, option)
                else:
                    book.alter(name, element)
            else:
                print(f"{name} is not in the booklet")

        elif command[0] == "open":
            name = input("name of the shortcut : ") if len(command) == 1 else command[1]
            exec_file(name)

        elif command[0].lower() == "hi":
            print("Oh finally someone ask me for my feeling !")

        elif command[0] == "exit" or command[0] == "ex":
            break

        else:
            if command[0] in book.booklet or path.exists(f"shortcuts/{command[0]}.py"):
                exec_file(command[0])
            else:
                print(f"the command '{command[0]}' is not recognized")

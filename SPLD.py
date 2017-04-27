"""
SPLD
----

This is a Shitty Python List Database that I am making just to learn and practice basic Python.
Features include creating, editing, displaying, and saving user created lists.

Author: Ginotuch
"""
from collections import defaultdict
from re import match


def menu_options():
    print("Create and edit lists")
    print("-"*len("Create and edit lists"))
    print("  1. Print list names")
    print("  2. Print list contents by name")
    print("  3. Print all lists and contents UNFINISHED")
    print("  4. Create new list")
    print("  5. Delete list")
    print("  6. Edit list IN PROGRESS")
    print("  7. Import list UNFINISHED")
    print("  8. Save database to file UNFINISHED")
    print("  9. Exit UNFINISHED (STILL WORKS)")


def user_input(maximum, exit_key, allowed_text):  # Choice selecting, also handles exiting/cancelling
    choice = None                                 # exit_key/allowed_text, will cancel/exit an operation.
    while choice is None:
        if allowed_text.lower() != "none":
            input_string = "Select your choice (\"" + allowed_text + "\" to cancel): "
        else:
            input_string = "Select your choice:"
        initial_input = input(input_string)
        try:
            choice = int(initial_input)
            while choice > maximum or choice < 0:
                if choice == exit_key:
                    break
                else:
                    print("Just read the damn options,", choice, "isn't an option")
                    choice = int(input("Select your choice: "))
        except ValueError:
            if (initial_input.isalpha()) and (initial_input.lower() == allowed_text.lower()) \
                    and initial_input.lower() != "none":
                if exit_key is None:  # This is here in case any number could be a valid option
                    return False
                else:
                    return exit_key
            else:
                print(" Invalid input")
    return choice


def store_in_list(list_name):
    count = None
    value_count = None
    temp_list = []
    while count is None:
        try:
            value_count = input("How many items do you want to store in \"" + list_name + "\"? (exit to cancel): ")
            if value_count.lower() == "exit":
                return None
            temp_count = int(value_count)
            if temp_count <= 0:
                print("Please select an amount above 0\n")
                continue
            count = temp_count
            for i in range(0, count):  # Gets value for the amount of items user wanted to store
                string = "Enter value: " + str(i + 1) + "/" + str(count) + ": "
                user_value = input(string)
                temp_list.append(user_value)
            return temp_list  # Returns the completed list
        except ValueError:
            print("", value_count, "is not a valid number.")
    return


def name_list(database):  # Names a newly created list (From option 3)
    banned_names = ["exit", "cancel", ""]
    found = None
    name = None  # This isn't needed, it's just so that pycharm stops complaining
    while found is None:
        name = str(input("Enter a list name: "))
        if name.lower() in banned_names:
            print("Name not allowed")
            continue
        elif not match("^[a-zA-Z0-9_.-]*$", name):
            print("Name must have characters, and no spaces or special characters.")
        elif name.lower() in (i.lower() for i in database):  # Checks if name exists in the database even if capitalized
            print("A list with that name already exists")
        else:
            found = True
    return name


def print_list_by_name(database):
    print("\n\nPrint list by name:")
    print("-" * len("Print list by name:"))
    list_name = check_list_exists(database, None)
    if list_name is None:  # If cancelled, returns.
        return
    # Prints the contents of the list separated by a comma (No brackets)
    print(list_name + ": ", ", ".join(str(x) for x in database[list_name]))


def print_list_names(database):
    print("\nCurrent lists:")
    for i in database:
        print(" -" + str(i))  # prints names of listed in format: "-list_name"


def create_a_list(database):
    print("\nCreate a list:")
    print("-" * len("Create a list:"))
    name = name_list(database)  # Gets name for list
    temp = store_in_list(name)  # Gets data for list, if user cancels then it will return with None
    if temp is not None:
        database[name] = temp
        print("Successfully created list")
        return database
    else:
        print("Cancelled")
        return None


def check_list_exists(database, previous_lists):
    found_list = None
    while found_list is None:  # Checks the database to make sure the list exists before continuing
        list_name = input("Enter list name (\"exit\" to cancel, \"list\" to print list names): ")
        if list_name.lower() == "exit":
            return
        elif list_name.lower() == "list":
            print_list_names(database)
        elif list_name not in database:
            print("That list doesn't exist")
        elif previous_lists is not None:
            if list_name.lower() in (i.lower() for i in previous_lists):
                print("You already selected that list.")
            elif list_name in database:
                return list_name
        elif list_name in database:
            return list_name


def delete_list(database):
    def delete_menu():
        print("\nDelete lists")
        print("-" * len("Delete lists"))
        print("  1. Print list names")
        print("  2. Print list contents by name")
        print("  3. Delete list by name")
        print("  9. Exit")
    delete_menu()
    option = 1
    while option <= 3:
        option = user_input(3, 9, "exit")
        if option == 1:
            print_list_names(database)
        elif option == 2:
            print_list_by_name(database)
            delete_menu()
        elif option == 3:
            checked_exists = check_list_exists(database, None)
            if checked_exists is not None:
                del database[checked_exists]
                print("Successfully deleted.")
                return database
            else:
                print("Cancelled")
                return
        elif option == 9:
            print("Cancelled")
            return


def check_database_size(database, minimum):  # Makes sure database is at least one.
    if len(database) < minimum:  # Checks if there are lists and exists current task if there are none
        print("Not enough lists in database, returning to menu.")
        return False
    else:
        return True


def nice_print(database, list_name):
    index_string = ""
    for x in range(0, len(database[list_name])):
        first_spaces = " " * (len(database[list_name][x]) // 2)
        second_spaces = " " * ((len(database[list_name][x]) - (len(database[list_name][x]) // 2)) + 1)
        index_string += first_spaces + str(x) + second_spaces
    string = []
    count = 1
    for x in database[list_name]:
        if count < 11:
            spaces = " "
        else:
            spaces = " " * (len(str(count)))
        string += [str(x) + "," + spaces]
        count += 1
    for i in string:
        print(i, sep="", end="")
    print("\n", index_string, sep="")
    print()


def edit_list(database):
    if check_database_size(database, 1) is True:
        def edit_menu():
            print("\nEdit lists")
            print("-" * len("Edit lists"))
            print("  1. Edit list by name")
            print("  2. Merge lists")
            print("  9. Exit")
        edit_menu()
        option = 1
        while option <= 2:
            option = user_input(2, 9, "exit")
            if option == 1:
                checked_exists = check_list_exists(database, None)  # Checks that the chosen list exists, then saves it
                if checked_exists is not None:
                    print("\nContents of", checked_exists + ":")
                    print(", ".join(str(x) for x in database[checked_exists]))

                    def edit_menu_2():
                        print("\nEditing:", checked_exists)
                        print("-" * len("Edit lists"))
                        print("  1. Delete an item")
                        print("  2. Add an item")
                        print("  3. Sort list (idk if I'll end up doing this)")  # Todo
                        print("  9. Exit")

                    edit_menu_2()
                    option_2 = 1  # This is just a choice tracker, it doesn't mean they selected menu option 2.
                    while option_2 <= 3:
                        option_2 = user_input(3, 9, "exit")
                        if option_2 == 1:
                            print("\nChose from the index which item is deleted from:", checked_exists)
                            option_3 = False
                            while not option_3:
                                nice_print(database, checked_exists)
                                option_3 = user_input((len(checked_exists) - 1), None, "exit")
                                if not option_3:
                                    print("\nCancelled")
                                    edit_menu_2()
                                    break
                                else:
                                    del database[checked_exists][option_3]
                                    print("\nSuccessfully deleted\nUpdated list:")
                                    nice_print(database, checked_exists)
                                    edit_menu_2()
                        elif option_2 == 2:
                            temp_list = store_in_list(checked_exists)
                            if temp_list is None:
                                edit_menu_2()
                                continue
                            for i in temp_list:
                                database[checked_exists].append(i)
                                print("\nSuccessfully added\nUpdated list:")
                                nice_print(database, checked_exists)
                            edit_menu_2()
                        elif option_2 == 3:
                            print("Print sort list")
                        elif option_2 == 9:
                            print("Cancelled")
                            edit_menu()
                else:
                    print(" Cancelled")
                    edit_menu()
            elif option == 2:
                if check_database_size(database, 2):
                    print_list_names(database)
                    choice = None
                    while choice is None:
                        merge_input = input("How many lists do you want to merge?: ")
                        try:
                            choice = int(merge_input)
                            while choice > len(database) or choice < 0:
                                print(" Invalid amount")
                                choice = int(input("How many lists do you want to merge? (\"exit\" to cancel): "))
                        except ValueError:
                            if (merge_input.isalpha()) and (merge_input.lower() == "exit"):
                                print("Cancelled")
                                edit_menu()
                                break
                            else:
                                print(" Invalid input")
                                continue
                        print("Selecting lists:")
                        selected_lists = []
                        user_cancelled = False
                        for i in range(0, choice):
                            temp = check_list_exists(database, selected_lists)
                            if temp is None:
                                user_cancelled = True
                                break
                            else:
                                selected_lists += [temp]
                        if user_cancelled:
                            print(" Cancelled")
                            edit_menu()
                            break
                        elif not user_cancelled:
                            new_list = []
                            for i in selected_lists:
                                for x in database[i]:
                                    new_list += [x]
                            print("Please enter a name for the combined list:")
                            new_name = name_list(database)
                            database[new_name] = new_list
                            print(" Successfully merged")
                            print("Newly created list:")
                            print(new_name + ":", ", ".join(str(x) for x in database[new_name]))
                            chosen = False
                            while not chosen:
                                delete_or_not = input("Delete the old lists that were merged? (Y/N): ").lower()
                                if delete_or_not == "y" or delete_or_not == "n":
                                    for i in selected_lists:
                                        del database[i]
                                    print("Deleted", merge_input, "lists")
                                    chosen = True
                                else:
                                    print(" Please type \"y\" or \"n\'")
                            edit_menu()
            elif option == 9:
                print(" Cancelled")
                edit_menu()
                return


def main():
    lists = defaultdict(list)
    menu_options()
    option = user_input(8, 9, "NONE")

    # For testing, creates temp lists
    test = 'test'
    lists[test] = ['ab', 'testing', 'word', 'characters', 'And other things']
    test = 'test2'
    lists[test] = ['this', 'is', 'another', 'test']
    test = 'test3'
    lists[test] = ['a', 'b', 'c', 'd']
    test = 'test4'
    lists[test] = ['e', 'f', 'g', 'h']

    # User choice selection till they decide to exit
    while option <= 8:
        if option == 1:  # print all names
            if check_database_size(lists, 1) is True:
                print_list_names(lists)
        elif option == 2:  # print contents from name
            if check_database_size(lists, 1) is True:
                print_list_by_name(lists)
        elif option == 3:  # print all lists and contents TODO
            print("todo 3")
            # Todo: Print all lists in columns, truncate if needed
        elif option == 4:  # Create a new list
            temp_lists = create_a_list(lists)
            if temp_lists is not None:
                lists = temp_lists
        elif option == 5:  # Delete list
            if check_database_size(lists, 1) is True:
                temp_lists = delete_list(lists)
                if temp_lists is not None:
                    lists = temp_lists
        elif option == 6:  # Edit a list TODO: Sorting
            edit_list(lists)
        elif option == 7:
            print("todo 7")
            # Todo: Import list
        elif option == 8:  # save
            if check_database_size(lists, 1) is True:
                print("Todo 0")
            # Todo: Save to file. Keeps history of last file, checks for overwrite.
            print("todo 9")
        elif option == 9:  # exit
            # Todo: Check for unsaved changes
            break
        print("\n")
        menu_options()
        option = user_input(8, 9, "NONE")
    print("\n\nk bye")


main()

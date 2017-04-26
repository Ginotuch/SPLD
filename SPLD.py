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
    choice = None
    while choice is None:
        input_string = "Select your choice: "
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
                print(" -Invalid input")
    return choice


def store_in_list(list_name):
    count = None
    temp_list = []
    while count is None:
        try:
            value_count = input("How many items do you want to store in \"" + list_name + "\"? (exit to cancel): ")
            if value_count == "exit":
                return None
            temp_count = int(value_count)
            if temp_count <= 0:
                print("Please select an amount above 0\n")
                continue
            count = temp_count
            for i in range(0, count):  # Gets value for the amount of items user wanted to store
                string = "What do you want to put in position " + str(i) + "? "
                user_value = input(string)
                temp_list.append(user_value)
            return temp_list  # Returns the completed list
        except ValueError:
            print("\nAll you had to do was enter a number\n")
    return


def name_list():  # Names a newly created list (From option 3)
    banned_names = ["exit", "cancel", ""]
    found = None
    name = None  # This isn't needed, it's just so that pycharm stops complaining
    while found is None:
        name = str(input("Enter a list name: "))
        if name.lower() in banned_names:
            print("Name not allowed")
            continue
        if not match("^[a-zA-Z0-9_.-]*$", name):
            print("Name must have characters, and no spaces or special characters.")
        else:
            found = True
    return name


def print_list_by_name(database):
    print("\n\nPrint list by name:")
    print("-" * len("Print list by name:"))
    list_name = check_list_exists(database)
    if list_name is None:  # If cancelled, returns.
        return
    # Prints the contents of the list separated by a comma (No brackets)
    print(list_name + ": ", ", ".join(str(x) for x in database[list_name]))


def print_list_names(database):
    print("\nCurrent lists:")
    for i in database:
        print(" -" + str(i))  # prints names of listed in format: "-list_name"


def create_a_list(database):  # Todo: Check if name already exists
    print("\nCreate a list:")
    print("-" * len("Create a list:"))
    name = name_list()  # Gets name for list
    temp = store_in_list(name)  # Gets data for list, if user cancels then it will return with None
    if temp is not None:
        database[name] = temp
        print("Successfully created list")
        return database
    else:
        print("Cancelled")


def check_list_exists(database):
    found_list = None
    while found_list is None:  # Checks the database to make sure the list exists before continuing
        list_name = input("Enter list name (\"exit\" to cancel, \"list\" to print list names): ")
        if list_name == "exit":
            return
        elif list_name == "list":
            print_list_names(database)
        elif list_name not in database:
            print("That list doesn't exist")
            continue
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
            checked_exists = check_list_exists(database)
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


def check_database_size(database):  # Makes sure database is at least one.
    if len(database) == 0:  # Checks if there are lists and exists current task if there are none
        print("No lists in database, returning to menu.")
        return False
    else:
        return True


def edit_list(database):
    if check_database_size(database) is True:
        def edit_menu():
            print("\nEdit lists")
            print("-" * len("Edit lists"))
            print("  1. Print list names")
            print("  2. Print list contents by name")
            print("  3. Edit list by name")
            print("  4. Merge lists UNFINISHED")  # Todo
            print("  9. Exit")
        edit_menu()
        option = 1
        while option <= 4:
            option = user_input(4, 9, "exit")
            if option == 1:
                print_list_names(database)
            elif option == 2:
                print_list_by_name(database)
                edit_menu()
            elif option == 3:
                checked_exists = check_list_exists(database)  # Checks that the chosen list exists, then saves it
                if checked_exists is not None:
                    print("\nContents of", checked_exists + ":")
                    print(", ".join(str(x) for x in database[checked_exists]))

                    def edit_menu_2():
                        print("\nEditing:", checked_exists)
                        print("-" * len("Edit lists"))
                        print("  1. Delete an item")
                        print("  2. Add an item")
                        print("  3. Sort list (idk if I'll end up doing this)")
                        print("  9. Exit")
                    edit_menu_2()
                    option_2 = 1  # This is just a choice tracker, it doesn't mean they selected menu option 2.
                    while option_2 <= 3:
                        option_2 = user_input(3, 9, "exit")
                        if option_2 == 1:
                            def nice_print(database_print, checked_exists_print):
                                print(", ".join(str(x) for x in database_print[checked_exists_print]))
                                # Puts index numbers under the center of each item in the selected list.
                                for x in range(0, len(database_print[checked_exists_print])):
                                    first_spaces = " " * (len(database_print[checked_exists_print][x]) // 2)
                                    second_spaces = " " * ((len(database_print[checked_exists_print][x]) -
                                                            (len(database_print[checked_exists_print][x]) // 2)) + 1)
                                    print(first_spaces + str(x) + second_spaces, end="")
                                print()
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
                                    print("\nSuccessfully deleted\nNew list:")
                                    nice_print(database, checked_exists)
                                    edit_menu_2()
                        elif option_2 == 2:
                            print("Add stuff")
                        elif option_2 == 3:
                            print("Print sort list")
                        elif option_2 == 9:
                            print("Cancelled")
                            edit_menu()
                else:
                    print(" Cancelled")
                    edit_menu()

            elif option == 4:
                print("Todo merge")
            elif option == 9:
                print(" Cancelled")
                edit_menu()
                return


def main():
    lists = defaultdict(list)
    menu_options()
    option = user_input(8, 9, "NONE")

    # For testing, creates temp list
    test = 'name'
    lists[test] = ['ab', 'testing', 'word', 'characters', 'And other things']

    # User choice selection till they decide to exit
    while option <= 8:
        if option == 1:  # print all names
            if check_database_size(lists) is True:
                print_list_names(lists)
        elif option == 2:  # print contents from name
            if check_database_size(lists) is True:
                print_list_by_name(lists)
        elif option == 3:  # print all lists and contents TODO
            print("todo 3")
            # Todo: Print all lists in columns, truncate if needed
        elif option == 4:  # Create a new list
            temp_lists = create_a_list(lists)
            if temp_lists is not None:
                lists = temp_lists
        elif option == 5:  # Delete list
            if check_database_size(lists) is True:
                temp_lists = delete_list(lists)
                if temp_lists is not None:
                    lists = temp_lists
        elif option == 6:  # Edit a list TODO: In progress
            edit_list(lists)
        elif option == 7:
            print("todo 7")
            # Todo: Import list
        elif option == 8:  # save
            if check_database_size(lists) is True:
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

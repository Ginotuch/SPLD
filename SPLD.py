"""
SPLD
----

This is a Shitty Python List Database that I am making just to learn and practice basic Python.
Features include creating, editing, displaying, and saving user created lists.

Author: Ginotuch
"""
from collections import defaultdict
from re import match
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from pickle import dump, load


def menu_options(unsaved):
    print("Create and edit lists")
    print("-"*len("Create and edit lists"))
    print("  1. Print list names")
    print("  2. Print list contents by name")
    print("  3. Print all lists and contents NOT DONE")
    print("  4. Create new list")
    print("  5. Delete list")
    print("  6. Edit list MOSTLY DONE")
    print("  7. Import database")
    print("  8. Save database to file")
    if unsaved[0] is True:
        print("  9. Exit*")  # Shows if there are unsaved changes
    elif not unsaved[0]:
        print("  9. Exit")


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


def yes_no(message=None, exit_word=None):
    if message is None:
        message = "Type yes or no (Y/N): "
    y_n_input = input(message).lower()
    if (y_n_input == exit_word) and (exit_word is not None):
        return
    while (y_n_input != 'y') and (y_n_input != 'n') and (y_n_input != "yes") and (y_n_input != "no"):
        print("Invalid input\n")
        y_n_input = input(message).lower()
    if (y_n_input == 'y') or (y_n_input == "yes"):
        return True
    elif (y_n_input == 'n') or (y_n_input == "no"):
        return False


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
    banned_names = ["exit", "cancel", "", "list"]
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
            checked_exists = check_list_exists(database, None)  # Checks that the list exists in the database
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


def check_database_size(database, minimum, no_print=False):  # Makes sure database is at least one.
    if len(database) < minimum:  # Checks if there are lists and exists current task if there are none
        if not no_print:
            print("Not enough lists in database, returning to menu.")
        return False
    else:
        return True


def nice_print(database, list_name):
    index_string = ""
    for x in range(0, len(database[list_name])):  # This is for creating the index numbers to print
        first_spaces = " " * (len(database[list_name][x]) // 2)  # Enough spaces to that the index number is centered
        second_spaces = " " * ((len(database[list_name][x]) - (len(database[list_name][x]) // 2)) + 1)  # Centers next
        index_string += first_spaces + str(x) + second_spaces
    string = []
    count = 1
    for x in database[list_name]:
        if count < 11:  # This is because "10" has two digits and messes with the spacing.
            spaces = " "
        else:
            spaces = " " * (len(str(count)))
        string += [str(x)]
        if count < 11:
            string += [","]
            string += [spaces]
            count += 1
        else:
            string += [","]
            string += [spaces]
            count += 1
    del string[-2]
    for i in string:
        print(i, sep="", end="")
    print("\n", index_string, sep="")


def edit_list(database, unsaved):
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
                        if option_2 == 1:  # Deletes an item
                            print("\nChose from the index which item is deleted from:", checked_exists)
                            option_3 = False
                            while not option_3:
                                nice_print(database, checked_exists)  # Prints out all items in the list, with indexes
                                option_3 = user_input((len(checked_exists)), None, "exit")
                                if option_3 is False:
                                    print("\nCancelled")
                                    edit_menu_2()
                                    break
                                else:
                                    del database[checked_exists][option_3]
                                    print("\nSuccessfully deleted\nUpdated list:")
                                    nice_print(database, checked_exists)
                                    unsaved[0] = True
                                    edit_menu_2()
                        elif option_2 == 2:  # Adds new item to list
                            temp_list = store_in_list(checked_exists)
                            if temp_list is None:
                                edit_menu_2()
                                continue
                            for i in temp_list:
                                database[checked_exists].append(i)
                            print("\nSuccessfully added\nUpdated list:")
                            unsaved[0] = True
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
                if check_database_size(database, 2):  # Makes sure there are at least two lists in the database to merge
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
                            if temp is None:  # Checks if the user has cancelled or not, if so the loop won't continue
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
                                new_list += database[i]
                            print("Please enter a name for the combined list:")
                            new_name = name_list(database)
                            database[new_name] = new_list
                            print(" Successfully merged")
                            unsaved[0] = True
                            print("Newly created list:")
                            print(new_name + ":", ", ".join(str(x) for x in database[new_name]))
                            chosen = False
                            while not chosen:
                                delete_or_not = input("Delete the old lists that were merged? (Y/N): ").lower()
                                if delete_or_not == "y":
                                    for i in selected_lists:
                                        del database[i]
                                    print("Deleted", merge_input, "lists")
                                    chosen = True
                                elif delete_or_not == "n":
                                    chosen = True
                                else:
                                    print(" Please type \"y\" or \"n\'")
                            edit_menu()
            elif option == 9:
                print(" Cancelled")
                edit_menu()
                return


def save_database(database):
    print("Please select save location...")
    root = Tk()
    root.attributes("-topmost", True)  # Puts save window at the top of all windows
    root.withdraw()  # Removes the root window (Just blank currently)
    save_location = asksaveasfilename(defaultextension=".spld", filetypes=(("SPLD database", "*.spld"),))
    root.destroy()
    if len(save_location) == 0:  # This handles if the user cancels on the file selection gui
        print("\nCancelled")
        return
    print(save_location)
    with open(save_location, "wb") as save_file:
        dump(database, save_file)
    print("\nSaved successfully")
    return True


def import_database(database):  # Mostly the same as save_database, check there for more comments
    print("\nImport database:")
    if check_database_size(database, 1, no_print=True):
        if not yes_no("This will overwrite the existing database, do you want to continue?(y/n): "):
            return
    print("Please select database location...")
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    open_location = askopenfilename(defaultextension=".spld", filetypes=(("SPLD database", "*.spld"),))  # File selector
    root.destroy()
    if len(open_location) == 0:
        print("\nCancelled")
        return
    with open(open_location, 'rb') as handle:
        database = load(handle)  # Replaces the current database with the imported one
    print("\nImported successfully")
    return database


def main():
    lists = defaultdict(list)
    unsaved = [False]  # Tracks unsaved changes, it's a list so that it can be changed within functions.
    menu_options(unsaved)
    option = user_input(8, 9, "NONE")

    # For testing, creates temp lists
    lists['test'] = ['ab', 'testing', 'word', 'characters', 'And other things']
    lists['test2'] = ['this', 'is', 'another', 'test']
    lists['test3'] = ['a', 'b', 'c', 'd']
    lists['test4'] = ['e', 'f', 'g', 'h']

    # User choice selection till they decide to exit
    while option <= 9:
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
                unsaved[0] = True
        elif option == 5:  # Delete list
            if check_database_size(lists, 1) is True:
                temp_lists = delete_list(lists)
                if temp_lists is not None:
                    lists = temp_lists
                    unsaved[0] = True
        elif option == 6:  # Edit a list TODO: Sorting
            edit_list(lists, unsaved)
        elif option == 7:
            importing = import_database(lists)
            if importing is not None:
                lists = importing
                unsaved[0] = False
        elif option == 8:  # save
            if check_database_size(lists, 1) is True:
                save_database(lists)
                unsaved[0] = False
        elif option == 9:  # exit
            if unsaved[0] is True:
                save_choice = yes_no("There are unsaved changes, do you want to save? (yes/no/cancel): ",
                                     exit_word="cancel")
                if save_choice:
                    if save_database(lists) is not None:
                        break
                if save_choice is None:
                    print("Cancelled")
                else:
                    break
            else:
                break
        print("\n")
        if len(lists) < 1:  # If there are no items in the list it will not say that here are unsaved changes.
            unsaved = [False]
        menu_options(unsaved)
        option = user_input(8, 9, "NONE")
    print("\n\nExiting")


main()

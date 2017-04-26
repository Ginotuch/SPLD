from collections import defaultdict


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
    print("  8. Exit UNFINISHED (STILL WORKS)")
    print("  0. Save database to file UNFINISHED")


def user_input(maximum):  # Get's user input for menu choice, repeats till acceptable range then returns choice.
    choice = None
    while choice is None:
        try:
            choice = int(input("Select your choice: "))
            while choice > maximum or choice < 0:
                print("Just read the damn options,", choice, "isn't an option")
                choice = int(input("Select your choice: "))
        except ValueError:
            print("\nEnter a number between 0 and", maximum, "(It's really not that hard)\n")
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
    banned_names = ["exit", "cancel", "", " ", "ben"]
    found = None
    name = None  # This isn't needed, it's just so that pycharm stops complaining
    while found is None:
        name = str(input("Enter a list name: "))
        if name in banned_names:
            print("Name not allowed")
            continue
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


def create_a_list(database):
    print("\nCreate a list:")
    print("-" * len("Create a list:"))
    name = name_list()  # Gets name for list
    temp = store_in_list(name)  # Gets data for list, if user cancels then it will return with None
    if temp is None:
        return
    else:
        database[name] = temp
        print(database)
        return database


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
        print("  0. Exit")
    delete_menu()
    option = 1
    while option <= 3:
        option = user_input(3)
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
        elif option == 0:
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
            print("  0. Exit")
        edit_menu()
        option = 1
        while option <= 3:
            option = user_input(3)
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
                    for x in range(0, len(database[checked_exists])):
                        first_spaces = " " * (len(database[checked_exists][x]) // 2)
                        second_spaces = " " * ((len(database[checked_exists][x]) - (len(database[checked_exists][x]) // 2)) + 1)
                        print(first_spaces + str(x) + second_spaces, end="")
                    print()

                    def edit_menu():
                        print("\nEditing:", checked_exists)
                        print("-" * len("Edit lists"))
                        print("  1. Print ldasfist names")
                        print("  2. Print lisasdft contents by name")
                        print("  3. Edit list by name")
                        print("  0. Exit")
                    edit_menu()
                    while option <= 3:
                        option = user_input(3)
                else:
                    print("Cancelled")
            elif option == 0:
                print("Cancelled")
                return


def main():
    lists = defaultdict(list)
    menu_options()
    option = user_input(8)
    test = 'name'
    lists[test] = ['ab', 'asadfasdbc', 'abcd', 'abcsdffde', 'abcdef']
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
            if temp_lists is None:
                print("Cancelled")
            else:
                lists = temp_lists
        elif option == 5:
            if check_database_size(lists) is True:
                lists = delete_list(lists)
        elif option == 6:  # Edit a list TODO
            edit_list(lists)
        elif option == 7:
            print("todo 7")
            # Todo: Import list
        elif option == 8:  # exit
            # Todo: Check for unsaved changes
            break
        elif option == 0:  # save
            if check_database_size(lists) is True:
                print("Todo 0")
            # Todo: Save to file. Keeps history of last file, checks for overwrite.
            print("todo 0")
        print("\n")
        menu_options()
        option = user_input(8)
    print("\n\nk bye")


main()

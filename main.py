from dataclasses import dataclass, field


@dataclass
class SplitWise:
    friends: dict[str, dict[str, float]] = field(
        default_factory=dict)  # Stores friend: (other_friend, amount_owed_to_other_friend)


def add_friends():
    num_friends = int(input("How many people would you like to add to the friend group? "))
    friend_list = dict()
    for x in range(num_friends):
        name = input(f"What is the name of friend #{x + 1}? ")
        friend_list[name] = dict()

    return friend_list


def show_friends(splitwise: SplitWise):
    if not splitwise.friends:
        print("No friends added yet!")
        return
    for friend, friends_that_owe in splitwise.friends.items():
        if not friends_that_owe:
            print(f"{friend}: \n\tCongratulations! You don't owe anyone money.")
        else:
            print(f"{friend}:")
            for friend_owe, amount in friends_that_owe.items():
                print(f"\tYou owe {friend_owe} ${amount:.2f}")


def remove_friends(splitwise: SplitWise):
    friend_list = splitwise.friends
    remove_name = input("Who would you like to remove from the friend list? ")

    # checks if friend is in friendlist
    if remove_name not in friend_list:
        print("This person doesn't exist. Please make sure you enter a name already in the friend group.")
    else:
        can_remove = True

        # can't remove if this person owes money
        if len(friend_list[remove_name]) != 0:
            can_remove = False
            print("You can't remove this person! They still owe the friend group money!")

        # can't remove if this person is owed money
        for friend in friend_list.values():
            if remove_name in friend:
                can_remove = False
                print("You can't remove this person! They are still owed money!")

        # remove friend if appropriate
        if can_remove:
            del friend_list[remove_name]

    return friend_list


def add_expense(splitwise: SplitWise):
    friend_list = splitwise.friends
    person_owed = input("Who is owed money? ")
    for friend, creditors in friend_list.items():

        # do not need to add amount owed to the person being owed
        if friend != person_owed:
            loop = True

            # loops until valid amount owed is entered
            while loop:
                loop = False
                amount_owed = input(f"How much money does {friend} owe {person_owed}? ")
                try:
                    amount_owed = float(amount_owed)
                except ValueError:
                    print(f"Error: Please enter a valid amount")
                    continue
                # loops if amount owed is a negative number
                if amount_owed < 0:
                    print("Please enter a positive number for amount owed.")
                    continue
                elif amount_owed > 0:
                    # checks if the friend already owes the person money; if money is already owed adds new amount
                    if person_owed in creditors:
                        creditors[person_owed] += amount_owed
                    else:
                        creditors[person_owed] = amount_owed


def register_payment(splitwise: SplitWise):
    payer = input("Enter the friend that paid the debt: ")
    if payer not in splitwise.friends:
        print(f"Error: {payer} is not registered with SplitWise!")
        return
    receiver = input("Enter the friend that received the payment: ")
    if receiver not in splitwise.friends:
        print(f"Error: {receiver} is not registered with SplitWise!")
        return
    if receiver not in splitwise.friends[payer]:
        print(f"Error: {payer} does not owe {receiver}, this payment will not be recorded!")
        return

    amount = input("Enter the amount paid: ")
    try:
        amount = float(amount)
    except ValueError:
        print(f"Error: Please enter a valid amount")
        return

    if splitwise.friends[payer][receiver] < amount:
        print(
            f"Warning: {payer} owes {receiver} {splitwise.friends[payer][receiver]:.2f} which is less than {amount:.2f}, the excess payment will be recorded as a debt from {receiver} to {payer}!")
        if payer in splitwise.friends[receiver]:
            splitwise.friends[receiver][payer] -= amount - splitwise.friends[payer][receiver]
        else:
            splitwise.friends[receiver][payer] = amount - splitwise.friends[payer][receiver]

    splitwise.friends[payer][receiver] = max(0., splitwise.friends[payer][receiver] - amount)
    if splitwise.friends[payer][receiver] == 0:
        del splitwise.friends[payer][receiver]


def menu():
    splitwise = SplitWise()
    while True:
        print("""Welcome to Splitwise! Please choose an option from the menu below, or enter 0 to exit:
1. Add Friends
2. Show Friends
3. Remove Friends
4. Add Expense
5. Register Payment
""")
        choice = input()
        try:
            choice = int(choice)
        except ValueError:
            print("Error: Please select a valid menu entry")
            continue

        if not 0 <= choice <= 5:
            print("Error: Please select a valid menu entry")
            continue

        match choice:
            case 0:
                print("Goodbye!")
                exit(0)
            case 1:
                new_friends = add_friends()
                splitwise.friends |= new_friends
            case 2:
                show_friends(splitwise)
            case 3:
                remove_friends(splitwise)
            case 4:
                add_expense(splitwise)
            case 5:
                register_payment(splitwise)


def main():
    menu()


if __name__ == '__main__':
    main()

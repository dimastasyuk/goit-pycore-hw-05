def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input):
    parts = user_input.split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and new phone please.")

    name, phone = args

    if name not in contacts:
        raise KeyError(name)

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    # Якщо ім'я не передали, виникне IndexError.
    name = args[0]

    if len(args) > 1:
        raise ValueError("Enter only user name.")

    # Якщо контакту немає, виникне KeyError.
    return contacts[name]


@input_error
def show_all(args, contacts):
    if args:
        raise ValueError("The all command does not need arguments.")

    if not contacts:
        return "No contacts found."

    result = ""

    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"

    return result.strip()


@input_error
def say_hello(args):
    if args:
        raise ValueError("The hello command does not need arguments.")

    return "How can I help you?"


@input_error
def close_bot(args):
    if args:
        raise ValueError("The exit and close commands do not need arguments.")

    return "Good bye!"


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(close_bot(args))

            if not args:
                break

        elif command == "hello":
            print(say_hello(args))

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(args, contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
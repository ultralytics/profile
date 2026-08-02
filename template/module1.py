# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license


def add_numbers(a, b):
    """Add two numbers together.

    Args:
        a (int | float): First number to add.
        b (int | float): Second number to add.

    Returns:
        (int | float): Sum of the input numbers.

    Examples:
        >>> add_numbers(1, 2)
        3
    """
    return a + b


def main():
    """Main entry point for the Ultralytics Template application.

    Executes a simple addition operation by calling the add_numbers function with predefined values. This function
    serves as a basic demonstration of program flow and function calling within the Ultralytics framework.

    Examples:
        >>> main()
        Added 1 + 2 = 3
    """
    a = 1
    b = 2
    y = add_numbers(a, b)
    print(f"Added {a} + {b} = {y}")


if __name__ == "__main__":
    main()

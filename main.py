import InterfaceManager as im


def main():
    # Initialize the user interface
    interface = im.InterfaceManager()

    # Run the user interface on a loop
    interface.start_interaction_loop()


if __name__ == "__main__":
    main()
import InterfaceManager as im
import ConfigManager as cm


def main():
    # Initialize the user interface
    # interface = im.InterfaceManager()

    # Run the user interface on a loop
    # interface.start_interaction_loop()

    manager = cm.ConfigManager()
    manager.create_substitution_dictionaries()
    # manager.load_ingredient_dictionary()

if __name__ == "__main__":
    main()
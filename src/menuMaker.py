import os
from pynput import keyboard

def select_menu_option(header, menu_options):
    current_option = 0
    stop_listener = False

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu():
        clear_screen()
        if header is not None:
            print(header)
        for idx, option in enumerate(menu_options):
            if idx == current_option:
                print("->", option)
            else:
                print("  ", option)

    display_menu()

    def on_press(key):
        nonlocal current_option, stop_listener

        try:
            if key == keyboard.Key.up:
                clear_screen()
                current_option = (current_option - 1) % len(menu_options)
                display_menu()
            elif key == keyboard.Key.down:
                clear_screen()
                current_option = (current_option + 1) % len(menu_options)
                display_menu()
            elif key == keyboard.Key.enter:
                stop_listener = True
                return False  # Stop the listener
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        while not stop_listener:
            listener.join()
    input()
    clear_screen()
    return current_option

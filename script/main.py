import unittest

import HtmlTestRunner


from character import create_character, load_character, load_characters, save_characters
from game import Game
from test.test import TestCharacterCreation

from leaderboard import Leaderboard
from visualization import FileHandler
from help import Helper
import pygame



def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def run_tests():
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCharacterCreation)

    # Using HtmlTestRunner to generate an HTML report
    runner = HtmlTestRunner.HTMLTestRunner(output='test_reports')
    result = runner.run(suite)


class Main:

    def __init__(self):
        self.current_username = None

    def get_username(self):
        return input("\033[92mDo Enter your username: ")

    def main(self):

        player_character = None
        print('\033[94m')
        FileHandler().display_text('../resources/welcome.txt')

        # welcome_banner()
        load_choice = input("\033[92mDo you want to load a previous game(L) or start a new one (N)? ").upper()

        while load_choice == "L":
            username = self.get_username()
            player_character = load_character(username)


            if player_character:

                print("\033[94m Character loaded successfully.")
                break
            else:
                print("\033[91m No saved character found. Enter the correct username.")

            # Ask for the username again
            username = self.get_username()
            player_character = load_character(username)

            if not player_character:
                load_choice = input("\033[92m Kindly start a new game (N) ").upper()

                if load_choice == "N":
                    player_character = create_character()
                else:
                    print('\033[91m Wrong option but we are creating a new player for you anyways')
                    player_character = create_character()

                # player_character = create_character()
        while load_choice == "N":
            player_character = create_character()

            break
        while load_choice != "N" and load_choice != "L":
            print('\033[91m Error: Please enter the right option L or N')
            load_choice = input("\033[92mDo you want to load a previous game (L) or start a new one (N)? ").upper()
            while load_choice == "L":
                username = self.get_username()

                player_character = load_character(username)
                if player_character:
                    print("Character loaded successfully.")
                    break
                else:
                    print("No saved character found..")
                    load_choice = input("kindly start a new game (N) ").upper()

                    # player_character = create_character()
            while load_choice == "N":
                player_character = create_character()  # No need to pass 'username' as an argument
                self.current_username = player_character.username  # Store the username for future use
                break

        def display_options():
            print("\033[92m\nOptions:")
            print("1. Go to North (Market)")
            print("2. Go to South (Alleyway)")
            print("3. Go to West")
            print("4. Check Inventory")
            print("5. Display Leaderboard")  # New option
            print("6. Help")
            print("7. Quit")

        def handle_user_choice(choice, user_character):
            if choice == '1':
                Game().start_market(user_character)
            elif choice == '2':
                Game().start_alleyway(user_character)
            elif choice == '3':
                Game().start_west(user_character)
            elif choice == '4':
                characters = load_characters()

                if user_character.username in characters:
                    characters[user_character.username] = {
                        "username": user_character.username,
                        "health": user_character.health,
                        "inventory": user_character.inventory,
                        "score": user_character.score,
                        "gun_score": user_character.gun_score,
                        "drug_score": user_character.drug_score,
                        "heist_wins": user_character.heist_wins,
                        "smuggling_wins": user_character.smuggling_wins
                    }

                    # Save the updated character information
                    save_characters(characters)

                    # Display the stats
                    user_character.display_stats()
                else:
                    print("\033[91mError: Character not found in the characters dictionary.")



            elif choice == '5':
                Leaderboard().display_leaderboard()
            elif choice == '6':
                Helper().display_help()
            elif choice == '7':
                Helper().quit()
            else:
                print("\033[91m Error: Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 or 5 or 6 or 7")

        while True:
            display_options()
            user_choice = input("Enter your choice: ")
            handle_user_choice(user_choice, player_character)

            # Add a check to save leaderboard before exiting
        # exit_choice = input("Do you want to save and exit the game (Y/N)? ").upper()
        # if exit_choice == 'Y':
        #     Leaderboard().save_leaderboard(Leaderboard().load_leaderboard())
        #     exit()





if __name__ == "__main__":

    sound_file_path = '../resources/audio/game_sound.mp3'
    play_sound(sound_file_path)

    try:
        play_sound(sound_file_path)

        while pygame.mixer.music.get_busy():
            # Updating the game or do other tasks while the sound is playing
            Main().main()

        # Stop the sound
        pygame.mixer.music.stop()

    except pygame.error as e:
        print(f"Er1ror playing the sound: {e}")
    # Run the tests
    # run_tests()
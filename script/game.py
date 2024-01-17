import random
from character import save_character, load_character
from leaderboard import Leaderboard
from visualization import FileHandler
from help import Helper


def check_winning_conditions(character):
    heist_wins = character.heist_wins
    smuggling_wins = character.smuggling_wins

    if heist_wins >= 1 and smuggling_wins >= 1:
        FileHandler().display_text('../resources/success.txt')
        exit_choice = input("Type Y to save and exit the game or any other letter to continue to top the leaderboard ").upper()
        if exit_choice == 'Y':
            Leaderboard().save_leaderboard(Leaderboard().load_leaderboard())
            exit()


def check_game_over(character):
    if character.health <= 0:
        # print("Game Over! Your character has run out of health.")
        FileHandler().display_text('../resources/game_over.txt')
        current_leaderboard = list(Leaderboard().load_leaderboard())  # Ensure it's a list
        new_entry = (character.username, character.score)
        updated_leaderboard = current_leaderboard + [new_entry]
        Leaderboard().save_leaderboard(updated_leaderboard, "../resources/leaderboard.json")
        Helper().quit()


class Game:

    def start_heist(self, character):
        print("\033[94m You embark on a daring bank heist.")
        # Set success_chance to 0.3 for a 30% chance
        is_gun = False
        for item in character.inventory:
            if item == 'Gun':
                is_gun = True
        # print(is_gun)
        success_chance = 0.99
        if random.uniform(0, 1) < success_chance and is_gun:
            FileHandler().display_text('../resources/bank_heist.txt')
            # print("Congratulations! You successfully completed the bank heist.")
            character.add_to_inventory("Stolen Money")
            character.score += 10  # Increase score by 10
            if character.health < 100:
                character.health += 10
            character.heist_wins += 1  # Increment heist wins
            save_character(character)
            Leaderboard().update_leaderboard(character.username, character.score)  # Update leaderboard
            check_winning_conditions(character)
        else:
            print('\033[91m')
            FileHandler().display_text('../resources/heist_health_lost.txt')
            # print("The bank heist failed. You attract unwanted attention and lose some health.")
            character.health -= 10
            character.score -= 5
            save_character(character)
            Leaderboard().update_leaderboard(character.username, character.score)
        print('\033[91m')
        check_game_over(character)

    def start_smuggling(self, character):
        is_drugs = False
        for item in character.inventory:
            if item == 'Drugs':
                is_drugs = True
        print("\033[94m You engage in a smuggling mission.")
        # Set success_chance to 0.5 for a 50% chance
        success_chance = 0.99

        if random.uniform(0, 1) < success_chance and is_drugs:
            FileHandler().display_text('../resources/smuggling.txt')
            # print("Congratulations! The smuggling mission was successful.")
            character.add_to_inventory("Contraband")
            character.score += 10  # Increase score by 10
            if character.health < 100:
                character.health += 10
            character.smuggling_wins += 1  # Increment smuggling wins
            save_character(character)
            Leaderboard().update_leaderboard(character.username, character.score)  # Update leaderboard
            check_winning_conditions(character)
        else:
            print('\033[91m')
            FileHandler().display_text('../resources/smuggling_health_lost.txt')
            # print("The smuggling mission failed. You attract unwanted attention and lose some health.")
            character.health -= 10
            character.score -= 5
            save_character(character)
            Leaderboard().update_leaderboard(character.username, character.score) # Update leaderboard
        print('\033[91m')
        check_game_over(character)

    def attempt_riddles(self, character, item):
        riddles = [
            {
                "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with the "
                            "wind. What am I?",
                "answer": "echo"
            },
            {
                "question": "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, "
                            "but water kills me. What am I?",
                "answer": "fire"
            },
            {
                "question": "The more you take, the more you leave behind. What am I?",
                "answer": "footsteps"
            },
            {
                "question": "I'm tall when I'm young, and short when I'm old. What am I?",
                "answer": "candle"
            },
            {
                "question": "I fly without wings. I cry without eyes. Wherever I go, darkness follows me. What am I?",
                "answer": "cloud"
            },
            # Add more riddles here
        ]

        for _ in range(10):
            riddle = random.choice(riddles)
            print("\033[92m \nTo buy the", item.lower() + ", you must answer this riddle:")
            print(riddle["question"])

            player_answer = input("\033[92mDo Your answer: ").strip().lower()
            normalized_answer = riddle["answer"].lower()

            if normalized_answer in player_answer:
                print('\033[94m', item)
                # print(f"Congratulations! You've successfully purchased the {item.lower()}.")
                if item.lower() == 'drugs':
                    FileHandler().display_text('../resources/drug.txt')
                if item.lower() == 'gun':
                    FileHandler().display_text('../resources/gun.txt')

                character.add_to_inventory(item)
                character.score += 10  # Increase score by 10
                save_character(character)
                Leaderboard().update_leaderboard(character.username, character.score)  # Update leaderboard
                return
            else:
                character.score -= 5
                print("\033[91m Incorrect answer. Try again. You have", 9 - _, "attempts left. ")

        print(f"You've run out of attempts. The {item.lower()} remains unsold.")
        player_character = load_character(character)
        check_game_over(player_character)

    def buy_drugs(self, character):
        print("Options:")
        print("1. Buy Drugs")
        print("2. Dangerous Move")
        print("3. Risky Move")
        print("4. Go Back")
        print("5. start smuggling")

        choice = input("\033[92mDo Enter your choice: ")

        if choice == '1':
            self.attempt_riddles(character, "Drugs")
        elif choice in ('2', '3'):
            print("You made a wrong choice. You lose 10 points.")
            character.score -= 10
            self.start_alleyway(character)
        elif choice == '4':
            print("You decide not to buy anything.")
        elif choice == '5':
            self.start_smuggling(character)
        else:
            print("\033[91m Error:Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 or 5.")
            self.buy_drugs(character)

    def buy_gun(self, character):
        print("Options:")
        print("1. Buy Gun")
        print("2. Dangerous Move")
        print("3. Risky Move")
        print("4. Go Back")
        print("5. Start Heist")

        choice = input("\033[92mDo Enter your choice: ")

        if choice == '1':
            self.attempt_riddles(character, "Gun")
        elif choice in ('2', '3'):
            print("\033[91m You made a wrong choice. You lose 10 points.")
            character.score -= 10
            self.start_market(character)
        elif choice == '4':
            print("You decide not to buy anything.")
        elif choice == '5':
            self.start_heist(character)
        else:
            print("\033[91m Error:Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 or 5")
            self.buy_gun(character)

    def start_alleyway(self, character):
        print("\033[94m You find yourself in a dark alleyway where you can purchase drugs.")
        print("\033[92m Options:")
        print("1. Go to North (Market)")
        print("2. Go to East")
        print("3. Go Back")
        print("4. Buy Drugs")
        print("5. Start smuggling")

        choice = input("\033[92mDo Enter your choice: ")

        if choice == '1':
            self.start_market(character)
        elif choice == '2':
            self.start_west(character)
        elif choice == '3':
            print("You decide to leave the dark alleyway.")
        elif choice == '4':
            self.buy_drugs(character)
        elif choice == '5':
            self.start_smuggling(character)
        else:
            print("\033[91m Error:Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 or 5")
            self.start_alleyway(character)

    def start_market(self, character):
        print("\033[94m You find yourself in a bustling market where you can purchase gun.")
        print("\033[92m Options:")
        print("1. Go to South (Alleyway)")
        print("2. Go to West")
        print("3. Check Inventory")
        print("4. Help")
        print("5. Buy Gun")
        print("6. Start Heist")

        choice = input("\033[92mDo Enter your choice: ")

        if choice == '1':
            self.start_alleyway(character)
        elif choice == '2':
            self.start_west(character)
        elif choice == '3':
            character.display_stats()
        elif choice == '4':
            Helper().display_help()
        elif choice == '5':
            self.buy_gun(character)
        elif choice == '6':
            self.start_heist(character)
        else:
            print("\033[91m Error: Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 or 5")
            self.start_market(character)

    def start_west(self, character):
        print("\033[94m You find yourself in the western part of the city which you connect to either market or "
              "alleyway.")
        print("\033[92m Options:")
        print("1. Go to South (Alleyway)")
        print("2. Go to North (Market)")
        print("3. Check Inventory")
        print("4. Help")

        choice = input("\033[92mDo Enter your choice: ")

        if choice == '1':
            self.start_alleyway(character)
        elif choice == '2':
            self.start_market(character)
        elif choice == '3':
            character.display_stats()
        elif choice == '4':
            Helper().display_help()
        else:
            print("\033[91m Error:Invalid choice. Try again with correct input of 1 or 2 or 3 or 4 ")
            self.start_west(character)

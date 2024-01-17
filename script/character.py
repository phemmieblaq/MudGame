import json
import random


def validate_height(height):
    try:
        # Try to convert the input to a float
        height_float = float(height)
        # Check if the height is within a valid range
        if 0 < height_float <= 300:
            return height_float
        else:
            print("\033[91mError:Invalid height. Please enter a height between 0 and 300.")
            return None
    except ValueError:
        print("\033[91mError:Invalid height format. Please enter a numeric value.")
        return None


# Function to validate gender input
def validate_gender(gender):
    # Check if the gender is one of the allowed values
    allowed_genders = ['male', 'female', 'Non-Binary', 'Other']
    if gender.lower() in allowed_genders:
        return gender.lower()
    else:
        print("\033[91mError:Invalid gender. Please enter 'male', 'female', 'Non-Binary', or 'other'.")
        return None


# Function to validate race input
def validate_race(race):
    # Check if the race is not empty
    if race.strip():
        return race
    else:
        print("\033[91mError:Invalid race. Please enter a non-empty value.")
        return None


def get_validated_input(prompt, validation_function):
    while True:
        user_input = input(prompt)
        validated_input = validation_function(user_input)
        if validated_input is not None:
            return validated_input


class Character:
    def __init__(self, username, health=20, inventory=None, score=0, gun_score=0, drug_score=0, heist_wins=0,
                 smuggling_wins=0):
        self.username = username
        self.health = health
        self.inventory = inventory if inventory else []
        self.score = score
        self.gun_score = gun_score
        self.drug_score = drug_score
        self.heist_wins = heist_wins
        self.smuggling_wins = smuggling_wins

    def display_stats(self):
        print(f"\033[94m\n{self.username}'s Stats:")
        print(f"Health: {self.health}")
        print(f"Inventory: {', '.join(self.inventory)}" if self.inventory else "Inventory is empty")
        print(f"Score: {self.score}")
        print(f"Heist Wins: {self.heist_wins}")
        print(f"Smuggling Wins: {self.smuggling_wins}")

    def add_to_inventory(self, item):
        self.inventory.append(item)


def character_exists(username, characters):
    return username in characters


def create_character():
    predefined_characters = {
        "Bloodfang": {"height": "3 feet", "gender": "Male", "race": "Human"},
        "Villain": {"height": "5.5 feet", "gender": "Female", "race": "Elf"},
        "Nightstalker": {"height": "5.8 feet", "gender": "Non-binary", "race": "Wizard"},
        "Darkmoon": {"height": "5.7 feet", "gender": "Male", "race": "Halfling"},
        "Ravenblood": {"height": "6.2 feet", "gender": "Female", "race": "Dwarf"}
    }

    print("\033[92mCreate a new character or choose a predefined character:")
    print("1. Choose a predefined character")
    print("2. Create a new character")

    while True:
        option = input("\033[92mEnter your choice (1 or 2): ")

        if option == "1":
            while True:
                print("\033[92mChoose a predefined character:")
                for index, character in enumerate(predefined_characters.keys(), start=1):
                    print(f"{index}. {character}")

                try:
                    choice = int(input("\033[92mEnter the number of the predefined character: "))
                    if choice < 1 or choice > len(predefined_characters):
                        raise ValueError("Invalid choice. enter 1 or2 or 3 or 4 or5")

                    username = list(predefined_characters.keys())[choice - 1]

                    characters = load_characters()
                    print(f"\033[94m {username}")
                    if character_exists(username, characters):
                        print("\033[91mError: Character with the selected username already exists. Choose another one.")
                        continue  # Continue the loop to prompt the user again

                    height, gender, race = predefined_characters[username].values()
                    new_character = Character(username, health=20)
                    save_character(new_character)
                    return new_character  # Return the instance of Character

                except (ValueError, IndexError):
                    print("\033[91mError: Invalid input. Please enter a valid number.")

        elif option == "2":
            while True:
                username = input("\033[92mEnter your unique username: ")
                characters = load_characters()

                if username.strip() != "" and not character_exists(username, characters):
                    break  # Exit the loop since a valid username is provided
                elif character_exists(username, characters):
                    print("\033[91mError: Character with the entered username already exists.")
                else:
                    print("\033[91mError: Username is empty. Please enter a unique username.")

            validated_height = get_validated_input("\033[92mEnter your height in cm: ", validate_height)
            validated_gender = get_validated_input("\033[92mEnter your gender: ", validate_gender)
            validated_race = get_validated_input("\033[92mEnter your race: ", validate_race)
            new_character = Character(username, health=20)
            save_character(new_character)
            return new_character  # Return the instance of Character





        else:
            print("\033[91mError: Invalid option. Please enter 1 0r 2")
            continue
        break


def save_character(character, filename="../resources/saved_characters.json"):
    characters = load_characters()
    characters[character.username] = {
        "username": character.username,
        "health": character.health,
        "inventory": character.inventory,
        "score": character.score,
        "gun_score": character.gun_score,
        "drug_score": character.drug_score,
        "heist_wins": character.heist_wins,
        "smuggling_wins": character.smuggling_wins
    }

    with open(filename, 'w') as file:
        json.dump(characters, file)
    print("\033[94m Character saved successfully.")


def load_character(username, filename="saved_characters.json"):
    characters = load_characters()
    character_data = characters.get(username)

    if character_data:
        return Character(
            username=character_data["username"],
            health=character_data["health"],
            inventory=character_data["inventory"],
            score=character_data["score"],
            gun_score=character_data["gun_score"],
            drug_score=character_data["drug_score"],
            heist_wins=character_data["heist_wins"],
            smuggling_wins=character_data["smuggling_wins"]
        )
    else:
        return None


def load_characters(filename="../resources/saved_characters.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_characters(characters, filename="../resources/saved_characters.json"):
    with open(filename, 'w') as file:
        json.dump(characters, file)

import json
import random

from character import load_characters, save_characters


class Leaderboard:

    def load_leaderboard(self, filename="../resources/leaderboard.json"):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def update_leaderboard(self, username, score):
        characters = load_characters()
        leaderboard = self.load_leaderboard()

        if username in characters:
            characters[username]["score"] = score
            save_characters(characters)  # Update the characters data
            leaderboard_entry = next((entry for entry in leaderboard if entry[0] == username), None)
            if leaderboard_entry:
                leaderboard_entry[1] = characters[username]["score"]
            else:
                leaderboard.append((username, characters[username]["score"]))

            self.save_leaderboard(leaderboard)  # Update the leaderboard
        else:
            print(f"User {username} not found in character data.")

    def save_leaderboard(self, leaderboard, filename="../resources/leaderboard.json"):
        with open(filename, 'w') as file:
            json.dump(leaderboard, file)

    def display_leaderboard(self):
        i = 1
        try:
            leaderboard = self.load_leaderboard()
            if not leaderboard:
                print("Leaderboard is empty.")
                return

            sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
            print("\033[94m\nLeaderboard:")
            for username, score in sorted_leaderboard:
                print(f"\033[94m {i}.  {username}:   {score}")
                i += 1

        except Exception as e:
            print(f"Error displaying leaderboard: {e}")

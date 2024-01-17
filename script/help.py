class Helper:
    def display_help(self) -> None:
        print("\nHelp:")
        print(
            "\033[94mTo buy a gun for your heist mission, you should go to the Market and solve the riddle to be able "
            "to buy a gun.")
        print(
            "To buy drugs for your contraband mission, you should go to the Alleyway and solve the riddle to be able "
            "to buy the drugs.")
        print("Giving wrong inputs will reduce your score.")
        print("failing to have key item in the inventory in order to start a mission attract health penalty ")
        print("failing each mission reduce your health")
        print("if your health reduce to zero , that is game over ")
        print("winning both heist mission and smuggling mission make you complete total mission ")
        print("Leaderboard will help you to check your score against the players.")
        print("Inventory will give you your statistics and your scores.")
        print("Riddle hint 1: It is something related to voice.")
        print("Riddle hint 2: It is something that is used to cook.")



    def quit(self):
        print("Exiting the game. Goodbye!")
        exit()

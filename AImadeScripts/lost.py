import random

def introduction():
    print("Welcome to 'Lost in the Woods'!")
    print("You find yourself in a dark and eerie forest, surrounded by tall trees and strange sounds.")
    print("Your goal is to find your way out of the forest before it's too late.")
    print()

def choose_path():
    print("You come across a fork in the road.")
    choice = input("Do you want to go left or right? (l/r): ").lower()  
    return choice

def bear_encounter():
    print("As you continue on the path, you encounter a ferocious bear!")
    decision = input("Do you want to run or play dead? (run/dead): ").lower()
    return decision

def win_game():
    print("Congratulations! You have successfully escaped from the forest. You are safe for now.")

def lose_game():
    print("Oh no! It seems like you've met a disastrous end in the forest. Maybe next time you will have better luck.")

def play_game():
    introduction()
    step_1 = choose_path()
    if step_1 == "l":
        step_2 = bear_encounter()
        if step_2 == "run":
            win_game()
        else:
            lose_game()
    else:
        lose_game()

play_game()

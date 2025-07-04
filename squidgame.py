import random

players = [] # list of all players

class Agent:
  def __init__(self, id, age, gender, morals, physical, mental, debt, stress, trauma, motiv, loyalty):
    self.id = id # player identification number

    self.age = age
    self.gender = gender

    self.morals = morals # morality
    self.physical = physical # physical abilities (0-100)
    self.mental = mental # mental abilities (0-100)

    self.debt = debt # player's debt

    self.stress = stress # stress levels
    self.trauma = trauma # trauma levels
    self.motiv = motiv # motivation

    self.loyalty = loyalty # how loyal you are to friends
    # self.similarity_bias = similarity_bias # bias to cooperating with similar people

  def kill(self, id):
    for player in players:
      if player.id == id:
        players.remove(player)

        break

    print(f"Player {self.id} has eliminated Player {player.id}")
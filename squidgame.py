import random

players = [] # number of players

class Agent:
  def __init__(self, id, morals, physical, mental, debt, stress, trauma, motiv, loyalty, similarity_bias):
    self.id = id # player identification number

    self.morals = morals # morality
    self.physical = physical # physical abilities (0-100)
    self.mental = mental # mental abilities (0-100)

    self.debt = debt # player's debt

    self.stress = stress # stress levels
    self.trauma = trauma # trauma levels
    self.motiv = motiv # motivation

    self.loyalty = loyalty # how loyal you are to friends
    self.similarity_bias = similarity_bias # bias to cooperating with similar people

  def chance(self, attr): # outputs True or False
    value = random.random()

    if value >= self.attr:
      return True
    
    return False
  
player1 = Agent()
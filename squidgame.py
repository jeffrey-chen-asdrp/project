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

  def relationship_chance(self, player): # returns 0-100
    age_dif = self.age - player.age # less difference equals higher chance

    if self.gender == player.gender:
      genders = 0

    else:
      genders = 15
    
    moral_dif = self.morals - player.morals # less difference equals higher chance
    mental_dif = self.mental - player.mental # less difference equals higher chance

    if 40 - abs(age_dif) < genders:
      age_gender_var = 0
    
    else:
      age_gender_var = 40 - abs(age_dif) - genders


    if 30 - abs(moral_dif) < 0:
      morals_var = 0

    morals_var = 30 - abs(moral_dif)


    if 30 - abs(mental_dif) < 0:
      mental_var = 0

    mental_var = 30 - abs(mental_dif)

    chance = age_gender_var + morals_var + mental_var

    return chance
  
Player1 = Agent(1, 36, "Male", 90, 70, 86, 1000, 2, 0, 60, 90)
Player2 = Agent(2, 51, "Male", 97, 96, 91, 100, 0, 0, 0, 0)

print(Player1.relationship_chance(Player2))
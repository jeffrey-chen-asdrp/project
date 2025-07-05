import random

players = [] # list of all players

class Agent:
  def __init__(self, id, age, gender, morals, physical, mental, debt, stress, motiv, loyalty):
    self.id = id # player identification number

    self.hp = 100 # starts with 100 but recovers over time

    self.age = age
    self.gender = gender

    self.morals = morals # morality
    self.physical = physical # physical abilities (0-100)
    self.mental = mental # mental abilities (0-100)

    self.debt = debt # player's debt

    self.stress = stress # stress levels
    self.motiv = motiv # motivation

    self.loyalty = loyalty # how loyal you are to friends
    # self.similarity_bias = similarity_bias # bias to cooperating with similar people

    self.inventory = [] # can include knives, punch, forks, etc, assume they all start with a knife

    self.relationships = [] # every player with a relationship would be modeled with [{"player": Agent, "strength": number}]
    self.voting_history = [] # tracks voting history

  def choose_violence(self, player): # chooses what action they take (punch, stab, choke, do nothing)
    # (<20<45 punch, <45<)
    # Morals 15%
    # Physical intimidation (difference from your trait and the player's trait along with age difference) 15%
    # Motivation 35%
    # Awareness 35% (awareness in understanding when to kill/attack)

    # self.awareness = 

    intimidation = self.physical - player.physical # positive value indicates you are not scared, negative means you are

    chance = 15 * (100-self.morals)/100 + 15 * intimidation/100 + 35 * self.motiv/100 + 35 * self.awareness/100

    return chance
    
    # Punch: hp - 10, gain stress, mental decreases, morals decrease, physical decrease, motiv increases
    # Stab: hp - 35, gain more stress, mental decreases more, morals decrease a lot, physical decreases a lot, motiv decreases a lot
    # Choke: hp - 100, survival chance 4%, if survives moral decreases, physical increases, stress increase, motiv increases

  def choke(self, id):
    for player in players:
      if player.id == id:
        players.remove(player)

        print(f"Player {self.id} has eliminated Player {player.id}")

        break

  def relationship_chance(self, player): # returns 0-100
    age_dif = abs(self.age - player.age) # less difference equals higher chance

    if self.gender == player.gender: 
      gender_dif = 0

    else:
      gender_dif = 15

    if 40 - age_dif < gender_dif:
      age_gender_var = 0
    
    else:
      age_gender_var = 40 - age_dif - gender_dif

    moral_dif = abs(self.morals - player.morals) # less difference equals higher chance
    mental_dif = abs(self.mental - player.mental) # less difference equals higher chance

    if 30 - moral_dif < 0:
      morals_var = 0

     morals_var = 30 - moral_dif

    if 30 - mental_dif < 0:
      mental_var = 0

    mental_var = 30 - mental_dif

    chance = age_gender_var + morals_var + mental_var

    return chance
  
  def build_relationship(self, player):
    if not(player in self.relationships):
      strength = self.relationship_chance(player)

      self.relationships.append({"player":player, "strength":strength})

      print(f"Player {self.id} has established a relationship with Player {player.id} of strength {strength}")

  def vote(self): # interval of 0-100, high number means higher chance of voting no
    # morals = 93
    # 35 * 0.93
    
    # stress = 30
    # 45 * 0.3

    # motiv = 25
    # 20 * 0.25

    chance = self.morals/100 * 35 + self.stress/100 * 45 + self.motiv/100 * 20

    if random.random() <= chance/100:
      self.voting_history.append("No")
      print(f"Player {self.id} has voted no")

      return "No"
    
    print(f"Player {self.id} has voted no")
    self.voting_history.append("Yes")

    return "Yes"

Player1 = Agent(1, 33, "Male", 93, 82, 80, 1000, 84, 80, 70)
Player2 = Agent(2, 41, "Male", 90, 82, 81, 66, 90, 17, 26)
# id, age, gender, morals, physical, mental, debt, motiv, loyalty

print(Player1.choose_violence(Player2))
class Agent:
  def __init__(self, id, age, gender, physical, charisma, obedience, revenge_tendency, morals, aggression):
    self.id = id

    self.age = age
    self.gender = gender

    self.physical = physical

    self.charisma = charisma
    self.obedience = obedience
    self.revenge_tendency = revenge_tendency

    self.morals = morals

    self.aggression = aggression

    self.relationships = [] # every player will be in the format {"player":player, "trust":value, "similarity":value}

  def calc_similarity(self, player):
    # age and gender = 35%
    # morals = 65%

    age_diff = abs(self.age - player.age)
    moral_diff = abs(self.morals - player.morals)

    if self.gender == player.gender:
      gender_diff = 0

    else:
      gender_diff = 15

    similarity = 100 - 1.2 * (0.35 * (age_diff + gender_diff) + 0.65 * moral_diff)

    return similarity
  

  def log_relationship(self, player, trust, similarity):
    for relationship in self.relationships:
      if relationship["player"] == player.id:
        self.relationships["trust"] == trust
        self.relationships["similarity"] == similarity

        return
      
  def update_trust(self, player, change):
    for relationship in self.relationships:
      if relationship["player"] == player.id:
        self.relationships["trust"] += change

        return
      
class Round:
  def __init__(self, agents, time):
    self.agents = agents
    self.voting = [] # {"id":player.id, "votes":[p2, p3]}

    self.time = time

    for agent in agents:
      self.voting.append({"id":agent.id, "votes":[]})

  def vote(self, p1, p2): # p1 votes for p2
    for agent in self.voting:
      if agent["id"] == p2.id:
        agent["votes"].append(p1)

        return
      
  def count_majority(self):
    


P1 = Agent(1, 20, "Male", 100, 100, 100, 100, 64, 100)
P2 = Agent(2, 47, "Female", 100, 100, 100, 100, 97, 100)
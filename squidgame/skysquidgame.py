import random

class Agent:
  def __init__(self, id, age, gender, physical, charisma, obedience, revenge_tendency, morals, aggression):
    self.id = id

    self.age = age
    self.gender = gender

    self.physical = physical # dicates who wins

    self.charisma = charisma # more likely for others to follow your vote
    self.obedience = obedience # more likely to vote for majority rather than the player with the lowest relationship strength
    self.revenge_tendency = revenge_tendency # more likely to vote for someone who voted for you

    # Obedience is 65%, revenge tendency is 15%, similarity bias is 10%, charisma is 10%

    # 3 people have voted, 2 people have voted for P1 while 1 person has voted for you

    self.morals = morals

    self.aggression = aggression

    self.trust = 70 # decreases by 15 every time someone votes for you (TBD)

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
  
  def calc_relationship(self, player):
    for relationship in self.relationships:
      if relationship["player"] == player:
        break

    strength = 0.65 * relationship["trust"] + 0.35 * self.calc_similarity(player)

    return strength
  
  def make_relationships(self, players):
    for player in players:
      if self.id != player.id:
        player.relationships.append({
          "player": player,
          "trust": player.trust,
          "similarity": self.calc_similarity(player),
        })

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
    self.voting = [] # {"player":player, "votes":[p2, p3]}

    self.time = time

    for agent in agents:
      self.voting.append({"player":agent, "votes":[]})

  def vote(self, p1, p2): # p1 votes for p2
    for agent in self.voting:
      if agent["player"] == p2:
        agent["votes"].append(p1)

        return
      
  def count_majority(self):
    agents = []
    votes = []

    for agent in self.voting:
      agents.append(agent["player"])
      votes.append(len(agent["votes"]))

    for vote in votes:
      index = votes.index(max(votes))

    return agents[index]
  
  def eliminate(self, player):
    self.agents.remove(player)

  def create_all_relationships(self): # for every player
    for player in self.agents:
      player.make_relationships(self.agents)

  def get_revenge(self, player): # {"player":player, "votes":[p2, p3]}
    targets = []

    for agent in self.voting:
      if agent["player"] != player:
        if player in agent["votes"]:
          targets.append(agent["player"])

    return targets # list
  
  def get_charisma(self, player):
    weights = []
    population = []

    for agent in self.agents:
      if agent != player:
        weights.append(agent.charisma)

    weights = sorted(weights)

    for weight in weights:
      for agent in self.agents:
        if agent != player:
          if agent.charisma == weight:
            population.append(agent)

            break

    if len(weights) >= 3: # give extra weights to top 3 agents with high charisma
      weights[-1] *= 2
      weights[-2] *= 1.5
      weights[-3] *= 1.2

    choice = random.choices(population=population, weights=weights)

    return choice[0] # since choice is in [choice] format, use choice[0] to exclude the list

  def round(self):
    self.create_all_relationships()

    players = random.shuffle(self.agents) # shuffles the order in which they go

    for index, player in enumerate(players):
      relationships = []
      relationship_strengths = []

      for relationship in self.relationships:
        relationships.append(relationship)
        relationship_strengths.append(player.calc_relationship(relationship["player"]))

      index = relationship_strengths.index(min(relationship_strengths))
      target = relationships[index]

      if index == 0: # check if player is first to vote
        self.vote(player, target)

      else:
        if player == self.count_majority(): # revenge 80% similarity 20%
          if random.random() <= 0.8: # selected revenge
            targets = self.get_revenge(player)
            target = random.choice(targets)

            self.vote(player, target)

          else: # similarity selected
            self.vote(player, target)

        else:
          if random.random() <= 0.65: # obedience selected lowkey should do random.choices
            target = self.count_majority()

            self.vote(player, target)

          elif random.random() <= 0.8: # revenge selected
            targets = self.get_revenge(player)
            target = random.choice(targets)

            self.vote(player, target)

          elif random.random() <= 0.9: # similarity bias selected
            self.vote(player, target)

          else: # charisma bias selected
            target = self.get_charisma(player)

            self.vote(player, target)

          




  #   surviving_players = []
  #   for player in players:
  #       survival_chance = player.physical/100
  #       if random.random() < survival_chance:
  #           surviving_players.append(player)
  #           print(f"Player {player.id} survived.")
  #       else:
  #           print(f"Player {player.id} was eliminated")
  #   print{f"\n {len(surviving_players)} players remain"}


P1 = Agent(1, 20, "Male", 100, 100, 100, 100, 64, 100)
P2 = Agent(2, 47, "Female", 100, 100, 100, 100, 97, 100)
P3 = Agent(3, 15, "Male", 98, 100, 70, 86, 97, 100)
P4 = Agent(4, 65, "Female", 100, 100, 80, 100, 97, 100)

game1 = Round([P1, P2, P3, P4], 90)
game1.round()
import random
import time

class Agent:
  def __init__(self, id, age, gender, physical, charisma, obedience, revenge_tendency, similarity_bias, charisma_bias, indecisiveness, morals, aggression): # all traits 1-100
    self.id = id

    self.age = age
    self.gender = gender

    self.physical = physical # dicates who wins

    self.charisma = charisma # more likely for others to follow your vote
    self.obedience = obedience # more likely to vote for majority rather than the player with the lowest relationship strength
    self.revenge_tendency = revenge_tendency # more likely to vote for someone who voted for you (50-100)

    self.similarity_bias = similarity_bias # (50-100)
    self.charisma_bias = charisma_bias

    self.indecisiveness = indecisiveness/2 # (0-50)

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
        self.relationships.append({
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

    for relationship in p2.relationships:
      if relationship["player"] == p1:
        relationship["trust"] -= 30

        if relationship["trust"] < 0:
          relationship["trust"] = 0

    self.has_voted.append(p1)

    time.sleep(3 * (1+p1.indecisiveness/100)) # minimum is three seconds
      
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
      if agent["player"] == player:
        return agent["votes"]
  
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
  
  def get_fighter(self):
    weights = []
    population = []

    for agent in self.agents:
      weights.append(agent.aggression)

    weights = sorted(weights)

    for weight in weights:
      for agent in self.agents:
        if agent.aggression == weight:
          population.append(agent)

          break

    if len(weights) >= 3: # give extra weights to top 3 agents with high charisma
      weights[-1] *= 2
      weights[-2] *= 1.5
      weights[-3] *= 1.2

    choice = random.choices(population=population, weights=weights)

    return choice[0] # since choice is in [choice] format, use choice[0] to exclude the list
  
  def get_victim(self):
    return random.choice(self.agents)

  def round(self):
    self.create_all_relationships()

    players = self.agents
    random.shuffle(players) # shuffles the order in which they go

    start = time.time()
    end = time.time()

    self.has_voted = []

    while end - start < self.time:
      for i, player in enumerate(players):
        relationships = []
        relationship_strengths = []

        for relationship in player.relationships:
          relationships.append(relationship["player"])
          relationship_strengths.append(player.calc_relationship(relationship["player"]))

        index = relationship_strengths.index(min(relationship_strengths))
        target = relationships[index]

        fight = False

        end = time.time()

        if end - start >= self.time * 2/3: # check if fight should happen
          chance = random.random()

          if chance <= 35:
            fight = True

            break

        if end - start >= self.time * 4/5:
          chance = random.random

          if chance <= 95:
            fight = True

            break

        if i == 0: # check if player is first to vote
          self.vote(player, target)

          print(f"Player {player.id} has voted for Player {target.id}")

        else:
          was_voted = False

          for agent in self.voting:
            if agent == player:
              if len(agent["votes"]) > 0:
                was_voted = True

                break
          
          if player == self.count_majority(): # revenge 80% similarity 20%
            # formula = random.choices(population=["P1","P2"], weights=[80*(1-(avg-value))])
            choice = random.choices(population=["revenge","similarity"], weights=[80*(1-(75-player.revenge_tendency)/100), 20*(1-(75-player.similarity_bias)/100)])
            
            if choice[0] == "revenge": # selected revenge 
              targets = self.get_revenge(player)
              target = random.choice(targets)

              self.vote(player, target)

              print(f"Player {player.id} has voted for Player {target.id}")

            else: # similarity selected
              self.vote(player, target)

              print(f"Player {player.id} has voted for Player {target.id}")

          else:
            if was_voted:
              choice = random.choices(population=["obedience","revenge","similarity","charisma"], weights=[65*(1-(75-player.obedience)/100), 15*(1-(75-player.revenge_tendency)/100), 10*(1-(75-player.similarity_bias)/100), 10*(1-(75-player.charisma_bias)/100)])

            else:
              choice = random.choices(population=["obedience","similarity","charisma"], weights=[50*(1-(75-player.obedience)/100), 25*(1-(75-player.similarity_bias)/100), 25*(1-(75-player.charisma_bias)/100)])
            
            if choice[0] == "obedience":
              target = self.count_majority()

              self.vote(player, target)

              print(f"Player {player.id} has voted for Player {target.id}")

            elif choice[0] == "revenge":
              targets = self.get_revenge(player)
              target = random.choice(targets)

              self.vote(player, target)

              print(f"Player {player.id} has voted for Player {target.id}")

            elif choice[0] == "similarity": # similarity bias selected
              self.vote(player, target)


              print(f"Player {player.id} has voted for Player {target.id}")

            else: # charisma bias selected
              target = self.get_charisma(player)

              self.vote(player, target)

              print(f"Player {player.id} has voted for Player {target.id}")

      if i+1 == len(players): # every player has voted
        player = self.count_majority() # majority player

        self.eliminate(player)

        print(f"Player {player.id} has been eliminated as the majority of the vote")

        self.survivors = self.agents

        return

      elif fight:
        fighter = self.get_fighter()
        victim = self.get_victim()

        if fighter.physical >= victim.physical:
          self.eliminate(victim)

          print(f"Player {victim.id} has been pushed off by Player {fighter.id} in a fight")

          for agent in self.agents:
            if agent != fighter:
              for relationship in agent.relationships:
                if relationship["player"] == fighter:
                  relationship["trust"] -= 25

          self.survivors = self.agents

          return

        else:
          self.eliminate(fighter)

          print(f"Player {fighter.id} has been pushed off by Player {victim.id} in a fight")

          self.survivors = self.agents

          return

      end = time.time()

    if len(players) == len(self.agents): # no players were eliminated within time
      for agent in self.agents:
        self.eliminate(agent) # every player ends up eliminated
        
        print(f"Player {agent.id} has been eliminated")

        self.survivors = self.agents

        return

players = []
id = 1

for i in range(20):
  # id, age, gender, physical, charisma, obedience, revenge_tendency, similarity_bias, charisma_bias, indecisiveness, morals, aggression

  age = random.randint(18, 70)
  gender = random.choice(["Male", "Female"])

  physical = random.randint(20, 100)

  charisma = random.randint(50, 100)
  obedience = random.randint(50, 100)
  revenge_tendency = random.randint(50, 100)
  similarity_bias = random.randint(50, 100)
  charisma_bias = random.randint(50, 100)

  indecisiveness = random.randint(1, 100)
  
  morals = random.randint(1, 100)

  aggression = random.randint(1, 100)

  player = Agent(id, age, gender, physical, charisma, obedience, revenge_tendency, similarity_bias, charisma_bias, indecisiveness, morals, aggression)
  players.append(player)

  id += 1

print("Round 1 starting...")  

game1 = Round(players, 120)
game1.round()

print("Round 2 starting...")

game2 = Round(game1.survivors, 120)
game2.round()

print("Round 3 starting...")

game3 = Round(game2.survivors, 120)
game3.round()
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt
import numpy as np
import random

class Fish:
  def __init__(self, age=0):
    self.age = age
    self.lifespan = random.randint(7, 8)

    self.gender = random.choice(["male", "female"])
    self.mated = False

    if self.gender == "female":
      self.offspring_count = random.randint(1,4)

    else:
      self.offspring_count = None
    
  def can_mate(self):
    return not(self.mated) and self.age in [3,4,5,6]
  
  def aging(self, years=1):
    self.age += years
  
def simulate_population(years, initial_fish):
  population = []
  trend = [] # [year, population]

  for i in range(initial_fish):
    age = random.randint(1,6)

    population.append(Fish(age=age))

  for year in range(years):
    females = []
    males = []

    for fish in population:
      fish.age += 1

      if fish.age == fish.lifespan:
        population.remove(fish)

      if fish.can_mate():
        if fish.gender == "female":
          females.append(fish)

        else:
          males.append(fish)

    random.shuffle(females)
    random.shuffle(males)

    for i in range(min(len(males), len(females))):
      female = females[i]
      male = males[i]

      offspring = female.offspring_count

      for _ in range(offspring):
        fish = Fish(age=0)

        population.append(fish)

      female.mated = True
      male.mated = True

    trend.append(len(population))

  return trend

years = 50
starting_pop = 150

trend = simulate_population(years, 150)

x = np.array(range(years))
y = np.array(trend)

fig, ax = plt.subplots()

plt.xlabel("Years")
plt.ylabel("Population")

plt.plot(x, y)

loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)

plt.savefig("trend.png")
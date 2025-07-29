import math

def sigmoid_scale(x):
  return 1 / (1 + math.exp(-0.1 * (x - 50)))  # returns ~0 to 1

trust_weight1 = 35 * sigmoid_scale(25)
trust_weight2 = 35 * sigmoid_scale(75)

print(trust_weight1)
print(trust_weight2)
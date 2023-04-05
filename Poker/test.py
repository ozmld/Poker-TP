from itertools import islice
from math import factorial
di = {"royal_flush": 0, "straight_flush": 0, "four_of_a_kind": 0, "full_house": 0,
     "flush": 0, "straight": 0, "three_of_a_kind": 0, "two_pairs": 0, "pair": 0, None: 0}
def c(n, k):
     return factorial(n) // factorial(k) // factorial(n - k)

print(c(13, 5) / c(52, 5) * 4)
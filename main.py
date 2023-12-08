import sys

from distance_matrix import DistanceMatrix
from branch_and_bound import BranchAndBound
from heuristics import Heuristics

if not sys.argv[1]:
    raise Exception()

distance_matrix = DistanceMatrix(sys.argv[1])
branch_and_bound = BranchAndBound(DistanceMatrix(sys.argv[1]))
heuristics = Heuristics(DistanceMatrix(sys.argv[1]))

print(f"Branch and Bound: {branch_and_bound.run()}")
print(f"Twice-around-the-tree: {heuristics.twice_around_the_tree()}")
print(f"Christofides: {heuristics.christofides()}")
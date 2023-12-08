import sys
import linecache
import ast
from distance_matrix import DistanceMatrix
from branch_and_bound import BranchAndBound
from heuristics import Heuristics

def run_tests(file_names):
    with open("test_results.txt", "w") as results_file:
        results_file.write("")  # Writing an empty string to clear the file

    with open("test_results.txt", "a") as results_file:
        for i, file_name in enumerate(file_names):
            print(f"Running tests for file: {file_name}")
            distance_matrix = DistanceMatrix(file_name)
            branch_and_bound = BranchAndBound(distance_matrix)
            heuristics = Heuristics(distance_matrix)

            bb_results = branch_and_bound.run()[0]
            tat_results = heuristics.twice_around_the_tree()[0]
            ch_results = heuristics.christofides()[0]
            
            results_file.write(f"Test {i+1}:\n")
            results_file.write(f"\tSolution for branch and bound: {bb_results}, TATT: {tat_results}, Christofides: {ch_results}\n")
            results_file.write(f"\tRatio TATT/BnB: {round(tat_results/bb_results, 3)}, Ratio Christofides/BnB: {round(ch_results/bb_results, 3)}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Please provide at least one file name.")

    file_names = sys.argv[1:]
    run_tests(file_names)
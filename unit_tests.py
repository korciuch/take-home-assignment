import sys
from tests import test1, test2, test3

TESTS = [test1, test2, test3]

def run_unit_tests():
    correct = 0
    for t in TESTS:
        correct += t()
    print("PASSED {}/{} TESTS".format(correct,len(TESTS)))

if __name__ == '__main__':
    run_unit_tests()
from tests import test1, test2, test3, test4

# List of tests to be evaluated

TESTS = [test1, test2, test3, test4]

# Checks correctness of basic test cases
def run_unit_tests():
    correct = 0
    for t in TESTS:
        result = t()
        correct += result
        if not result:
            print("\nFAILED: ", t, '\n')
        else:
            print("\nPASSED: ", t, '\n')

    print("PASSED {}/{} TESTS".format(correct, len(TESTS)))


# Entrypoint for unit_tests.py

if __name__ == '__main__':
    run_unit_tests()

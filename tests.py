from utils import Shape
from solve import main


def test1() -> bool:
    expected_result = set([
        'film', 'lif', 'lim', 'mil'
    ])
    result = main(random_seed=1, shape=Shape(2, 2))
    sect = expected_result.intersection(set(result))
    if len(sect) == len(expected_result):
        return True
    else:
        return False


def test2() -> bool:
    expected_result = set([
        'flip', 'film', 'fill', 'fip', 'lif',
        'lija', 'lif', 'lip', 'lipa', 'ill', 'jill',
        'jap', 'lap', 'film', 'fill', 'fip', 'pilm',
        'pill', 'pal', 'pall', 'palli', 'palm', 'all',
        'alp'
    ])
    result = main(random_seed=1, shape=Shape(3, 3))
    sect = expected_result.intersection(set(result))
    if len(sect) == len(expected_result):
        return True
    else:
        return False


def test3() -> bool:
    expected_result = set([
        'lim', 'film', 'mijl', 'plim', 'mil', 'jim', 'lif'
    ])
    result = main(random_seed=1, shape=Shape(4, 2))
    sect = expected_result.intersection(set(result))
    if len(sect) == len(expected_result):
        return True
    else:
        return False


def test4() -> bool:
    expected_result = set([
        'imp', 'fip', 'pim'
    ])
    result = main(random_seed=1, shape=Shape(2, 4))
    sect = expected_result.intersection(set(result))
    if len(sect) == len(expected_result):
        return True
    else:
        return False

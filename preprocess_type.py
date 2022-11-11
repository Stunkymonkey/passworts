"""collection of types"""

from collections import defaultdict


def integer_dict():
    """
    these lines are required, because pickle does not store the data type
    https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multipile-modules
    """
    return defaultdict(int)

def flatten(l):
    """Flatten a list of lists"""
    return [item for sublist in l for item in sublist]


def len_longest_ith_item(items, i):
    """Return the length of the longest ith item in the list of tuples"""
    return max(map(lambda tup: len(tup[i]), items))

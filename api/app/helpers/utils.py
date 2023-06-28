from Levenshtein import distance
from typing import List


def most_similar(target: str, candidates: List[str]) -> int:
    """
    Find candidate with smallest LCS edit distance to target.

    Args:
        target (str)
        candidates (List[str])

    Returns:
        int: Index of candidate array.

    Example:
        >>> target = "kitten"
        >>> candidates = ["sitting", "mitten", "mittens", "kit", "kitchen"]
        >>> most_similar(target, candidates)
        3
    """
    distances = [distance(target, candidate) for candidate in candidates]
    min_distance = min(distances)
    min_index = distances.index(min_distance)
    return min_index


def find_key(key: str, data: list, target: str) -> int:
    """
    Get index where key matches target in a list of dictionaries.

    Args:
        key (str): Key
        data (list): List of dictionaries.
        target (str): Target value

    Returns:
        int: Index, default 0

    Raises:
        ValueError: If the data list is empty.

    Examples:
        >>> data = [{'name': 'John', 'age': 25}, {'name': 'Jane', 'age': 30}]
        >>> find_key('name', data, 'Jane')
        1
        >>> find_key('age', data, '25')
        0
    """
    if not data:
        raise ValueError("Data is empty.")
    for i, item in enumerate(data):
        if item.get(key) == target:
            return i
    return 0


def deep_get(dictionary, keys):
    """
    Recursively get a dict value from a list of keys.

    Args:
        dictionary (dict): The dictionary to search.
        keys (list): A list of keys to traverse the dictionary.

    Examples:
        >>> data = {'name': ['John'], 'age': 25}
        >>> deep_get(data, ['name', 0])
        'John'
    """
    value = dictionary

    for key in keys:
        try:
            value = value[key]
        except (KeyError, TypeError):
            return None

    return value

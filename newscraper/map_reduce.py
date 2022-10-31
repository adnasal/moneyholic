def map_fnc(word):
    return word, 1


def map_string(text):
    words = text.split()

    map_obj = map(map_fnc, words)

    return map_obj


def reduce(map_obj):
    result = {}
    for obj in map_obj:
        word = obj[0]
        if result.get(word):
            result[word] += 1
            continue
        else:
            result[word] = 1

    return result

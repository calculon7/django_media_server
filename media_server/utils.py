def get_sort_name(name: str):
    if not name:
        return None

    ignore_words = [
        'a',
        'an',
        'the',
    ]

    words = name.split(' ')

    # index of first word not in ignore_words or 0
    idx = next((i for i, word in enumerate(words) if (word.lower() not in ignore_words)), 0)

    return ' '.join(words[idx:])

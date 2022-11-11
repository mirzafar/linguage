import random


def get_random_words(list_id):
    l = random.sample(list_id, len(list_id))
    return l
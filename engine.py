"""
the middle-man engine

allows me to break doww dict better for the pynecone to handel them better

plus can be used a as json handler and holder user data

"""

def get_values(plant) -> list:
    tmp = []
    for v in plant.values():
        tmp.append(v)
    return tmp


def get_keys(plant) -> list:
    tmp = []
    for k in plant.keys():
        tmp.append(k)
    return tmp

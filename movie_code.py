import random

def generate_move_code():
    sonlar = []

    # Birinchi son: 1–9 (0 bo‘lmasin)
    sonlar.append(random.randint(1, 9))

    # Qolgan 2 ta son: 0–9, lekin takrorlanmasin
    while len(sonlar) < 3:
        son = random.randint(0, 9)
        if son not in sonlar:
            sonlar.append(son)

    kod = "".join(map(str, sonlar))
    return kod

import random
import os

random.seed(42)

ALPHABET = list('abcdefghijklmnopqrstuvwxyz')

def random_string(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

def write_input(path, chars, values, A, B):
    with open(path, 'w') as f:
        f.write(f"{len(chars)}\n")
        for c in chars:
            f.write(f"{c} {values[c]}\n")
        f.write(A + "\n")
        f.write(B + "\n")

os.makedirs("data", exist_ok=True)

test_configs = [
    #(alphabet_size, len_A, len_B)
    (4,  25,  25),
    (4,  30,  30),
    (5,  40,  35),
    (6,  50,  50),
    (6,  60,  55),
    (8,  75,  80),
    (8,  100, 90),
    (10, 120, 110),
    (10, 150, 140),
    (26, 200, 200),
]

for i, (alpha_size, lenA, lenB) in enumerate(test_configs, 1):
    chars = ALPHABET[:alpha_size]
    values = {c: random.randint(0, 20) for c in chars}
    A = random_string(lenA, chars)
    B = random_string(lenB, chars)
    path = f"data/test{i:02d}.in"
    write_input(path, chars, values, A, B)
    print(f"Generated {path}  |A|={lenA}  |B|={lenB}  alphabet={chars}")

print("\nDone.")

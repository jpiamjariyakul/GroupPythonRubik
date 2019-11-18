import random
def main():
    a = ["G", "G", "G"]

    d = ["R", "R", "R"]

    g = ["B", "B", "B"]

    j = ["O", "O", "O"]

    dump = [d, g, j]

    layer_2 = random.choice(dump)
    layer_3 = layer_2

    face = [a, layer_2, layer_3]
    turn = 0
    print(*face, sep="\n")

    if layer_2 == d:
        turn = 3
    if layer_2 == g:
        turn = 2
    if layer_2 == j:
        turn = 1
        
    print(str(turn) + " turn is required")

main()

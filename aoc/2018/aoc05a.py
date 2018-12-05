#!/usr/bin/python3


def get_polarity(char):
    return char in "abcdefghijklmnopqrstuvwxyz"


def main():
    sequence = list(open("aoc05.txt").read().strip())
    #sequence = list("dabAcCaCBAcCcaDA")
#    print("".join(sequence))
    while True:
        skip_next = False
        new_sequence = []

        for idx, char in enumerate(sequence[:-1]):
            if skip_next:
                skip_next = False
                continue

            next_char = sequence[idx+1]
            if char.lower() == next_char.lower() and char.isupper() != next_char.isupper():
                skip_next = True
                continue

            new_sequence.append(char)

        if not skip_next:
            new_sequence.append(sequence[-1])

#        print("".join(new_sequence))

        if new_sequence == sequence:
            break
        else:
            sequence = new_sequence

    print("".join(sequence))
    print(len(sequence))
if __name__ == "__main__":
    main()

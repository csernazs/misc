#!/usr/bin/pypy


def get_polarity(char):
    return char in "abcdefghijklmnopqrstuvwxyz"


def main():
    original_sequence = list(open("aoc05.txt").read().strip())
    #original_sequence = list("dabAcCaCBAcCcaDA")
#    print("".join(original_sequence))
    chars_to_remove = sorted(set([x.lower() for x in original_sequence]))
    print(chars_to_remove)

    min_length = None
    for char_to_remove in chars_to_remove:
        print(char_to_remove)
        sequence = [x for x in original_sequence if x.lower() != char_to_remove]

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

        print(len(sequence))
        if min_length is None or len(sequence) < min_length:
            min_length = len(sequence)

    print(min_length)

if __name__ == "__main__":
    main()

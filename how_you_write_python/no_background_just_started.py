
def get_value(pair):
    return pair[1]

def main():
    words = {}
    for line in open("input.txt"):
        line = line.strip()
        for word in line.split():
            word = word.lower()
            if word in words:
                words[word] += 1
            else:
                words[word] = 1


    word_list = list(words.items())
    word_list.sort(key=get_value)

    for word, cnt in list(reversed(word_list))[:10]:
        print(cnt, word)


if __name__ == "__main__":
    main()


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


    for word, cnt in sorted(words.items(), key=lambda kv: kv[1], reverse=True)[:10]:
        print(cnt, word)


if __name__ == "__main__":
    main()

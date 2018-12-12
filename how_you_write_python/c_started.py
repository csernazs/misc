BUFFSIZE = 1024

def to_lower(char):
    code = ord(char)
    if ((code >= 65) and (code <= 90)):
        code = code + 32
        return chr(code)

    return char

def add_word(words, word):
    if (word in words):
        words[word] += 1
    else:
        words[word] = 1

def main():
    f = open("input.txt")

    buff = None
    word = ""
    words = {}
    while True:
        buff = f.read(BUFFSIZE)
        if (buff == ""):
            break

        for i in range(len(buff)):
            char = buff[i]
            if ((char == " " or char == "\n") and word != ""):
                add_word(words, word)
                word = ""

            elif (char != " " and char != "\n"):
                word += char
    f.close()


    if (len(word) > 0):
        add_word(words, word)

    word_list = []
    for word, cnt in words.items():
        word_list.append((cnt, word))

    word_list.sort(reverse=True)

    for i in range(10):
        print("%d %s" % word_list[i])


if (__name__ == "__main__"):
    main()

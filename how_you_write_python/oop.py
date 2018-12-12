class File:
    def __init__(self, path):
        self.__path = path
        self.__handle = None

    def getFileHandle(self):
        if self.__handle == None:
            self.__handle = open(self.__path, "r")

        return self.__handle

    def getPath(self):
        return self.__path


class BufferedReader:
    def __init__(self, file, buffsize=1024):
        self.__file = file
        self.__buffsize = buffsize

    def getBuffSize(self):
        return self.__buffsize

    def setBuffSize(self, value):
        self.__buffsize = value

    def getFile(self):
        return self.__file

    def readBuffer(self, buffer):
        for char in self.__file.getFileHandle().read(self.__buffsize):
            buffer.append(char)


class WordReader:
    def __init__(self, reader):
        self.__reader = reader
        self.__currentWord = None
        self.__buffer = []

    def getReader(self):
        return self.__reader

    def getCurrentWord(self):
        return self.__currentWord

    def readNextWord(self):
        word = ""

        while True:
            try:
                c = self.__buffer.pop(0)
            except:
                self.__reader.readBuffer(self.__buffer)
                try:
                    c = self.__buffer.pop(0)
                except:
                    self.__currentWord = word
                    return False

            if (c == "\n" or c == " "):
                if word != "":
                    self.__currentWord = word
                    return True
                continue

            word += c


class StringIterator:
    def __init__(self, string):
        self.__string = string
        self.__pos = -1

    def getCurrentChar(self):
        return self.__string[self.__pos]

    def getPosition(self):
        return self.__pos

    def nextChar(self):
        if self.__pos > len(self.__string) - 2:
            return False
        else:
            self.__pos += 1
            return True


class CharConverter:
    @staticmethod
    def toLower(char):
        code = ord(char)
        if ((code >= 65) and (code <= 90)):
            code = code + 32
            return chr(code)

        return char


class LowerCaseConverterIterator(StringIterator):
    def getCurrentChar(self):
        return CharConverter.toLower(super().getCurrentChar())


class StringBuilder:
    def __init__(self, iterator):
        self.__iterator = iterator

    def getIterator(self):
        return self.__iterator

    def buildString(self):
        buffer = ""
        while self.__iterator.nextChar():
            buffer += self.__iterator.getCurrentChar()

        return buffer


class CounterResult:
    def __init__(self, item, count):
        self.__item = item
        self.__count = count

    def getItem(self):
        return self.__item

    def getCount(self):
        return self.__count

    def isItemSet(self):
        return self.__item is not None


class Counter:
    def __init__(self):
        self.__items = {}

    def addItem(self, item):
        if item in self.__items:
            self.__items[item] += 1
        else:
            self.__items[item] = 1


    def getTopItem(self):
        maxcount = 0
        maxitem = None
        for item in self.__items.keys():
            count = self.__items[item]
            if count > maxcount:
                maxcount = count
                maxitem = item

        return CounterResult(maxitem, maxcount)

    def removeItem(self, counterresult):
        assert counterresult.isItemSet()
        self.__items.pop(counterresult.getItem())


class Application:
    @staticmethod
    def main():
        file = File("input.txt")
        br = BufferedReader(file)
        wr = WordReader(br)

        counter = Counter()
        while wr.readNextWord():
            lcci = LowerCaseConverterIterator(wr.getCurrentWord())
            sb = StringBuilder(lcci)
            counter.addItem(sb.buildString())

        for i in range(10):
            cr = counter.getTopItem()
            if cr.isItemSet():
                print(cr.getCount(), cr.getItem())
            else:
                break
            counter.removeItem(cr)


if __name__ == "__main__":
    Application.main()

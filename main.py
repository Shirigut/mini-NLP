import csv
import pathlib
import xml.etree.ElementTree as ET


def parse_syntax(file_name, syntax, counter):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        for p in perek:
            for word in p[1]:
                if word.attrib.get('phraseId') is not None and not word.attrib.get('phraseId') in syntax.values():
                    syntax[counter] = word.attrib['phraseId']
                    counter += 1
    return syntax, counter


def parse_xml(file_name, words, counter):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        for p in perek:
            for word in p:
                if word.text is not None and not word.text in words.values():
                    words[counter] = word.text
                    counter += 1
    return words, counter


def create_words_hashmap():
    words = {}
    syntax = {}
    counter1 = 0
    counter2 = 0

    for path in pathlib.Path("Torah").iterdir():  ##torah
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    for path in pathlib.Path("Prophets").iterdir():  ##neviim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    for path in pathlib.Path("Writings").iterdir():  ##ktuvim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    # f = open('bible_words.csv', 'w', encoding="utf8")  ##writing to csv file
    # writer = csv.writer(f)
    # for key, value in words.items():
    #     writer.writerow([key, value])
    # f.close()

    k = open('bible_syntax.csv', 'w', encoding="utf8")
    writer = csv.writer(k)
    for key, value in syntax.items():
        writer.writerow([key, value])
    k.close()



##want to extract the psukim that we taged from the xml in order to create our verctors
def create_psukim_set():
    print("hi")


if __name__ == '__main__':
    create_words_hashmap()










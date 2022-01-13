import csv
import os
import pathlib
import xml.etree.ElementTree as ET

words = {}

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
    counter = 0

    for path in pathlib.Path("Torah").iterdir():  ##torah
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter)
            words = words_new
            counter = counter_new

    for path in pathlib.Path("Prophets").iterdir():  ##neviim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter)
            words = words_new
            counter = counter_new

    for path in pathlib.Path("Writings").iterdir():  ##ktuvim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter)
            words = words_new
            counter = counter_new

    f = open('bible_words.csv', 'w', encoding="utf8")  ##writing to csv file
    writer = csv.writer(f)
    for key, value in words.items():
        writer.writerow([key, value])
    f.close()

    return words

##want to extract the psukim that we taged from the xml in order to create our verctors
def create_psukim_set():
    print("hi")

if __name__ == '__main__':
    words_hashmap = create_words_hashmap()








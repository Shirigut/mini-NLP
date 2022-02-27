import csv
import json
import pathlib
import xml.etree.ElementTree as ET
import re


def two_windows(syntax_vectors,data):
    counter = 0
    vector_output=[]
    for vector1 in syntax_vectors:
        vector = [a for a in vector1 if a!='']
        vector_pasuk=[]
        original_pasuk=data[str(counter)]
        pasuk_len = len(original_pasuk)
        vector_len = len(vector)
        al_id = find_al_id(original_pasuk)
        word_index = original_pasuk.index(al_id)

        if (vector_len != pasuk_len):
            vector_output.append([])
            counter = counter + 1
        else:
            if word_index >= 2:
                vector_pasuk.append(int(vector[word_index - 2]))
                vector_pasuk.append(int(vector[word_index - 1]))
                vector_pasuk.append(int(vector[word_index]))
            else:
                if word_index == 1:
                    vector_pasuk.append(-1)
                    vector_pasuk.append(int(vector[word_index - 1]))
                    vector_pasuk.append(int(vector[word_index]))
                else:
                    vector_pasuk.append(-1)
                    vector_pasuk.append(-1)
                    vector_pasuk.append(int(vector[word_index]))

            if word_index == pasuk_len - 1:
                vector_pasuk.append(-1)
                vector_pasuk.append(-1)
            else:
                if word_index == pasuk_len - 2:
                    vector_pasuk.append(int(vector[word_index + 1]))
                    vector_pasuk.append(-1)
                else:
                    vector_pasuk.append(int(vector[word_index + 1]))
                    vector_pasuk.append(int(vector[word_index + 2]))
            vector_output.append(vector_pasuk)
            counter = counter + 1

    return vector_output


def one_window(syntax_vectors,data):
    counter = 0
    vector_output=[]
    for vector1 in syntax_vectors:
        vector = [a for a in vector1 if a!='']
        vector_pasuk=[]
        original_pasuk=data[str(counter)]
        pasuk_len = len(original_pasuk)
        vector_len = len(vector)
        al_id = find_al_id(original_pasuk)
        word_index = original_pasuk.index(al_id)

        if (counter == 299):
            ()
        if (vector_len != pasuk_len):
            vector_output.append([])
            counter = counter + 1
        else:
            if word_index > 0:
                vector_pasuk.append(int(vector[word_index-1]))
            else:
                vector_pasuk.append(-1)
            vector_pasuk.append(int(vector[word_index]))

            if word_index == pasuk_len - 1:
                vector_pasuk.append(-1)
            else:
                vector_pasuk.append(int(vector[word_index + 1]))

            vector_output.append(vector_pasuk)
            counter = counter + 1

    return vector_output


def create_csv(output):
    with open('morph_new_two_windows.csv', 'w') as f:
        counter = 0
        for key in output:
            f.write("%s\n"%(str(output[counter]).replace('[', '').replace(']', '')))
            counter = counter + 1


def create_dictionary(csv_file):
    output = {}
    for row in csv_file:
        if row != [] and row is not None and len(row) > 1 and row[0] != "":
            output[row[1]] = int(row[0])
    return output


def search_syntax_pasuk(file_name, my_perek, my_pasuk, dict):
    pasuk_output = []
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        if my_perek == perek.attrib['DisplayName_Heb'][4:]:
            for p in perek:
                if my_pasuk == p.attrib['DisplayName_Heb'][5:]:
                    for i in range(len(p)):
                        if len(p[i]) > 0:
                            word = p[i][0]
                            if word.attrib.get('phraseId') is not None:
                                id = word.attrib.get('phraseId')
                                pasuk_output.append(dict[id])
                    return pasuk_output

def search_morph_pasuk(file_name, my_perek, my_pasuk, dict):
    pasuk_output = []
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        if my_perek == perek.attrib['DisplayName_Heb'][4:]:
            for p in perek:
                if my_pasuk == p.attrib['DisplayName_Heb'][5:]:
                    for i in range(len(p)):
                        if len(p[i]) > 0:
                            word = p[i]
                            if word.attrib.get('dtoken') is not None:
                                id = word.attrib.get('dtoken').partition("__")[2]
                                pasuk_output.append(dict[id])
                    return pasuk_output


def search_root_pasuk(file_name, my_perek, my_pasuk, dict):
    pasuk_output = []
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        if my_perek == perek.attrib['DisplayName_Heb'][4:]:
            for p in perek:
                if my_pasuk == p.attrib['DisplayName_Heb'][5:]:
                    for i in range(len(p)):
                        if len(p[i]) > 0:
                            word = p[i]
                            if word.attrib.get('root') is not None:
                                id = word.attrib.get('root')
                                pasuk_output.append(dict[id])
                    return pasuk_output


def search_lemma_pasuk(file_name, my_perek, my_pasuk, dict):
    pasuk_output = []
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        if my_perek == perek.attrib['DisplayName_Heb'][4:]:
            for p in perek:
                if my_pasuk == p.attrib['DisplayName_Heb'][5:]:
                    for i in range(len(p)):
                        if len(p[i]) > 0:
                            word = p[i]
                            if word.attrib.get('lemma') is not None:
                                id = word.attrib.get('lemma')
                                pasuk_output.append(dict[id])
                    return pasuk_output


def create_vectors(file, function, file_to_write):
    pasuk_output = []
    count = 0
    counter = 0

    file_psukim = open('all- on.csv', encoding='utf8')
    psukim = csv.reader((file_psukim))

    dict = create_dict(file)

    for row in psukim:
        if counter != 0:
            print(counter)
            row = str(row).split(",")
            book = row[3][2:-1]
            perek = row[2].replace('"', "").replace(' ', '').replace("'", '')
            pasuk = row[1].replace('"', "").replace(' ', '').replace("'", '')
            for path in pathlib.Path("all").iterdir():
                if path.is_file():
                    book_name = path.name.replace(".xml", "")
                    if book == book_name:
                        pasuk_list = function(path, perek, pasuk, dict)
                        pasuk_output.append(pasuk_list)
                        break
        counter += 1
    pasuk_output = [i for i in pasuk_output if i]
    with open(file_to_write, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerows(pasuk_output)


def parse_syntax(file_name, syntax, counter):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        for p in perek:
            for i in range(len(p)):
                if (len(p[i])>0):
                    word = p[i][0]
                    if word.attrib.get('phraseId') is not None and not word.attrib.get('phraseId') in syntax.values():
                        syntax[counter] = word.attrib['phraseId']
                        counter += 1
    return syntax, counter

def parse_morph(file_name, morph, counter):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    for perek in book:
        for p in perek:
            for word in p:
                if word.attrib.get('dtoken') is not None:
                    idd = word.attrib.get('dtoken').partition("__")[2]
                    if idd not in morph.values():
                        morph[counter] = idd
                        counter += 1
    return morph, counter


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


def create_morph_hashmap():
    morph = {}
    counter2 = 0

    for path in pathlib.Path("Torah").iterdir():  ##torah
        if path.is_file():
            morph_new, counter2_new = parse_morph(path, morph, counter2)
            morph = morph_new
            counter2 = counter2_new

    for path in pathlib.Path("Prophets").iterdir():  ##neviim
        if path.is_file():
            syntax_new, counter2_new = parse_morph(path, morph, counter2)
            morph = morph_new
            counter2 = counter2_new

    for path in pathlib.Path("Writings").iterdir():  ##ktuvim
        if path.is_file():
            morph_new, counter2_new = parse_morph(path, morph, counter2)
            syntax = morph_new
            counter2 = counter2_new

    f = open('bible_morph.csv', 'w', encoding="utf8")
    writer = csv.writer(f)
    for key, value in morph.items():
        writer.writerow([key, value])
    f.close()


def create_syntax_hashmap():
    syntax = {}
    counter2 = 0

    for path in pathlib.Path("Torah").iterdir():  ##torah
        if path.is_file():
            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    for path in pathlib.Path("Prophets").iterdir():  ##neviim
        if path.is_file():
            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    for path in pathlib.Path("Writings").iterdir():  ##ktuvim
        if path.is_file():
            syntax_new, counter2_new = parse_syntax(path, syntax, counter2)
            syntax = syntax_new
            counter2 = counter2_new

    f = open('bible_syntax.csv', 'w', encoding="utf8")
    writer = csv.writer(f)
    for key, value in syntax.items():
        writer.writerow([key, value])
    f.close()


def create_words_hashmap():
    words = {}
    counter1 = 0

    for path in pathlib.Path("Torah").iterdir():  ##torah
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

    for path in pathlib.Path("Prophets").iterdir():  ##neviim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

    for path in pathlib.Path("Writings").iterdir():  ##ktuvim
        if path.is_file():
            words_new, counter_new = parse_xml(path, words, counter1)
            words = words_new
            counter1 = counter_new

    f = open('bible_words.csv', 'w', encoding="utf8")  ##writing to csv file
    writer = csv.writer(f)
    for key, value in words.items():
        writer.writerow([key, value])
    f.close()


def csv_to_dict(psukim=None):
    psukim_list = []

    for row in psukim:
        row = str(row).split(",")
        pasuk = row[0]
        # cleaning the psukim
        pasuk = pasuk.replace('׃', '')
        pasuk = pasuk.replace('־', ' ')
        pasuk = pasuk.replace('[', '')
        pasuk = pasuk.replace(']', '')
        pasuk = pasuk.replace("'", '')
        pasuk = pasuk.replace("׀", '')
        pasuk = pasuk.replace("׀", '')
        pasuk = pasuk.replace("\\xa0", ' ')
        pasuk = re.sub(r"\([^()]*\)", '', pasuk)

        psukim_list.append(pasuk)

    # throw the header
    psukim_list = psukim_list[1:]
    return psukim_list


#create dict from csv
def create_dict(file):
    file_bible = open(file, encoding='utf8')
    bible_f = csv.reader((file_bible))
    dict = create_dictionary(bible_f)
    return dict

if __name__ == '__main__':
    create_words_hashmap()
    create_syntax_hashmap()
    create_morph_hashmap()
    create_vectors('bible_syntax.csv', search_syntax_pasuk, 'syntax_vectors.csv')
    create_vectors('bible_morph.csv', search_morph_pasuk,'morph_vectors.csv')
    create_vectors('bible_roots.csv', search_root_pasuk, 'root_vectors.csv')
    create_vectors('bible_lemma.csv', search_lemma_pasuk, 'lemma_vectors.csv')
    file_syntax_vectors = open('morph_vectors_newnew.csv', encoding='utf8')

    syntax_vectors = csv.reader(file_syntax_vectors)
    with open('word_embeddings_for_all_1000_al_psukim.json') as psukim_list:
        data = json.load(psukim_list)
        result_two_windows = two_windows(syntax_vectors,data)
        create_csv(result_two_windows)
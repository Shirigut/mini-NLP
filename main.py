import xml.etree.ElementTree as ET


def parse_xml(file_name):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    book = myroot[1][0]
    counter = 0
    words = {}
    for perek in book:
        for p in perek:
            for word in p:
                if word.text is not None and not word in words:
                    words[counter] = word.text
                    counter += 1



if __name__ == '__main__':
    parse_xml('Genesis.xml')

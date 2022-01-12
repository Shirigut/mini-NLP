import xml.etree.ElementTree as ET


def parse_xml(file_name):
    mytree = ET.parse(file_name)
    myroot = mytree.getroot()
    psukim = myroot[1][0][0]

if __name__ == '__main__':
    parse_xml('Genesis.xml')

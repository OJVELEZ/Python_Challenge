import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET


def insert


ns = {'ns': 'urn:ebay:apis:eBLBaseComponents'}
tree = ET.parse('./resource/categories_short.xml')
root = tree.getroot()
print(root.tag)
# print([elem.tag for elem in root.iter()])
# print(ET.tostring(root, encoding='utf8').decode('utf8'))
count = root.find('ns:CategoryCount', ns)
uptime = root.find('ns:UpdateTime', ns)
cversion = root.find('ns:CategoryVersion', ns)
rpriceallowed = root.find('ns:ReservePriceAllowed', ns)
minpriceallowed = root.find('ns:MinimumReservePrice', ns)
xmltimestamp = root.find('ns:Timestamp', ns)
xmlack = root.find('ns:Ack', ns)
xmlversion = root.find('ns:Version', ns)
xmlbuild = root.find('ns:Build', ns)
print(count.text)


# for category in root.iter('{urn:ebay:apis:eBLBaseComponents}Category'):
#     categoryid = category.find('ns:CategoryID', ns)
#     bestoffer = category.find('ns:BestOfferEnabled', ns)
#     autopay = category.find('ns:AutoPayEnabled', ns)
#     categorylevel = category.find('ns:CategoryLevel', ns)
#     categoryname = category.find('ns:CategoryName', ns)
#     categoryparent = category.find('ns:CategoryParentID', ns)


# for child in root:
#     print(child.tag, child.attrib)


# for category in tree.iterfind(".//Category"):
#     print(f"tag {category.tag}, Text: {category.text}")

# for category in tree.iter():
#     print(f"tag {category.tag}, Text: {category.text},{category.}")

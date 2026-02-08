import xml.etree.ElementTree as ET
from collections import Counter

path = r"C:\Users\feder\Downloads\federicomantua.WordPress.2026-02-08.xml"

ns = {}
for event, elem in ET.iterparse(path, events=("start-ns",)):
    ns[elem[0]] = elem[1]
print(ns)

tree = ET.parse(path)
root = tree.getroot()
item_types = Counter()
for item in root.findall(".//item"):
    post_type = item.findtext(f"{{{ns.get('wp')}}}post_type", default="")
    status = item.findtext(f"{{{ns.get('wp')}}}status", default="")
    item_types[(post_type, status)] += 1
print(item_types.most_common(20))

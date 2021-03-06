import xml.etree.ElementTree as ET



def parse_and_remove(filename, path):
   path_parts = path.split('/')
   doc = ET.iterparse(filename, ('start', 'end'))
   # Skip root element
   next(doc)
   tag_stack = []
   elem_stack = []
   for event, elem in doc:
    if event == 'start':
      tag_stack.append(elem.tag)
      elem_stack.append(elem)
    elif event == 'end':
                if tag_stack == path_parts:
                    yield elem
                try:
                    tag_stack.pop()
                    elem_stack.pop()
                except IndexError:
                    pass



governments = set()
countries = parse_and_remove('mondial-3.0.xml', 'country')
for country in countries:
    name = country.attrib['government']
    governments.add((name))

for government in sorted(governments):
    print(government.strip())
    







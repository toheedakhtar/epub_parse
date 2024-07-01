from zipfile import ZipFile
import os 
import xml.etree.ElementTree as ET

epub_path = "/home/toheed/Projects/epub_parse/linear-algebra.epub"
if not epub_path:
    epub_path = str(input('Input ePub path: '))   

# fetching opf from epub's META-INF
def get_opf_path(path):
    epub_name = path.split('/')[-1].split('.')[0]
    
    #unzipping epub
    with ZipFile(epub_path) as zipobj:
        zipobj.extractall(path = str(epub_name))

    dir_name = epub_name
    md_dir = os.listdir(dir_name)
    if 'META-INF' in md_dir :
        os.chdir(dir_name + '/META-INF')
        curr_dir = os.getcwd()
        for file in os.listdir(curr_dir):
            end = file.split('.')
            if end[1] == 'xml':

                with open(file) as f:
                    c_xml = f.read()
            else:
                print('container.xml file missing')

        # parsing opf path from xml
        root = ET.fromstring(c_xml)
        namespace = {'ns': 'urn:oasis:names:tc:opendocument:xmlns:container'} 
        full_path = root.find('.//ns:rootfile', namespace).attrib['full-path'] 
                
        # exit from META-INF to parent-dir where epub is extracted
        extr_dir = os.path.dirname(os.getcwd())
        
        return extr_dir, full_path 

    else:
        print('no META-INF directory')


def get_metadata(extr_dir , full_path):
    opf_path = extr_dir + '/' + full_path

    with open(opf_path) as opf:
        opf_data = opf.read()
    
    root = ET.fromstring(opf_data)
    # Define namespaces
    namespaces = {'opf': 'http://www.idpf.org/2007/opf','dc': 'http://purl.org/dc/elements/1.1/'}

    # parsing metadata elements
    metadata = root.find('opf:metadata', namespaces)
    title = metadata.find('dc:title', namespaces).text
    creator = metadata.find('dc:creator', namespaces).text
    identifier = metadata.find('dc:identifier',namespaces).text

    print(f"Title : {title}\nCreator : {creator}\nIdentifier : {identifier}")

    

extr_dir, full_path = get_opf_path(epub_path)
get_metadata(extr_dir , full_path)

'''
# getting to ocf file
path = '/home/toheed/Projects/epub_parse/epub3/'   # where epub is stored
epub_path = '/home/toheed/Projects/epub_parse/linear-algebra.epub'   # epub path
epub_name = epub_path.split('/')[-1].split('.')[0]      # epub name

# unzipping epub file

with ZipFile(epub_path) as zipobj:
    zipobj.extractall(path = str(epub_name))

dir_name = epub_name            # where epub is extracted , rn where epub is

md_dir = os.listdir(dir_name)
if 'META-INF' in md_dir:
    os.chdir(dir_name + '/META-INF')

    curr_dir = os.getcwd()      #inside META-INF
    #print(curr_dir)
    # print(os.listdir(curr_dir))

    for file in os.listdir(curr_dir):
        end = file.split('.')
        if end[1] == 'xml':
            # print(file)    # container.xml
            with open(file) as f:
                data = f.read()


# parsing manifest 
# finding the manifest section
manifest = root.find('opf:manifest', namespaces)

# Iterate over each item in the manifest
for item in manifest:
    href = item.attrib['href']
    item_id = item.attrib['id']
    media_type = item.attrib['media-type']
    properties = item.attrib.get('properties', '')

    if media_type == 'application/xhtml+xml':
        ch_path = content_dir + '/' + href
        print(ch_path)
        print('\n')
        with open(ch_path) as xhtml_f:
            ch_text = xhtml_f.read()
        
        #parsing text from xhtml

        root = ET.fromstring(ch_text)

        # finding the body element
        body = root.find('.//{http://www.w3.org/1999/xhtml}body')

        # If body found
        if body is not None:
            inner_text = ET.tostring(body, encoding='unicode', method='text')
            print(inner_text)
        else:
            print("No <body> element found in the XML content.")
        


        print('\n')
    
#        break;
    # print(f"Item ID: {item_id}, Href: {href}, Media Type: {media_type}, Properties: {properties}")

    # testing xhtml rendering 
    

print('\n\n')

# parsing spine 
#print('PRINTING SPINE.......\n')
#spine = root.find('opf:spine', namespaces)

#for itemref in spine:
#   idref = itemref.attrib['idref']
#    linear = itemref.attrib.get('linear', 'yes')  # default value for linear attribute is 'yes'

#    print(f"Itemref ID: {idref}, Linear: {linear}")


'''












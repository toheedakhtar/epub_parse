from zipfile import ZipFile
import os 
import xml.etree.ElementTree as ET

# getting to ocf file

epub_path = '/home/toheed/Projects/epub_parse/moby-dick.epub'
epub_name = epub_path.split('/')[-1].split('.')[0]

# unzipping epub file

with ZipFile(epub_path) as zipobj:
    zipobj.extractall(path = str(epub_name))

#dir_name = 'moby-dick'          # epub dir  

dir_name = epub_name

md_dir = os.listdir(dir_name)
if 'META-INF' in md_dir:
    os.chdir(dir_name + '/META-INF')

    curr_dir = os.getcwd()      #inside META-INF
    #print(curr_dir)
    # print(os.listdir(curr_dir))

    for file in os.listdir(curr_dir):
        end = file.split('.')
        if end[1] == 'xml':
            print(file)
            with open(file) as f:
                data = f.read()

# getting .ocf path from container
root = ET.fromstring(str(data))
# Define the namespace
namespace = {'ns': 'urn:oasis:names:tc:opendocument:xmlns:container'}

# Find the rootfile element and extract the full-path attribute value
full_path = root.find('.//ns:rootfile', namespace).attrib['full-path']

ocf_path = dir_name + '/' + full_path
print(ocf_path)

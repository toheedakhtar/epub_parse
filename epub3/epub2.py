from zipfile import ZipFile
import os 
import xml.etree.ElementTree as ET

epub_path = "/home/toheed/Projects/epub_parse/moby-dick.epub"
if not epub_path:
    epub_path = str(input('Input ePub path: '))   

#namespaces or xml parsing of ocf data
namespaces = {'opf': 'http://www.idpf.org/2007/opf','dc': 'http://purl.org/dc/elements/1.1/'}


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
        extr_dir = os.path.dirname(os.getcwd()) # where epub is extracted / unzipped
        opf_path = extr_dir + '/' +full_path   # path to package.opf file
        
        sep = '/'
        content_path = sep.join(opf_path.split('/')[:-1]) + '/'

        return opf_path , content_path

    else:
        print('no META-INF directory')

def get_opf_data(opf_path):
    with open(opf_path) as opf:
        opf_data = opf.read()
        return opf_data

def get_metadata(opf_data, root, namespaces):
    metadata_items = []
    # parsing metadata elements
    metadata = root.find('opf:metadata', namespaces)
    title = metadata.find('dc:title', namespaces).text
    creator = metadata.find('dc:creator', namespaces).text
    identifier = metadata.find('dc:identifier',namespaces).text
    
    metadata_item = {
            'title':title,
            'creator':creator,
            'identifier': identifier
            }

    metadata_items.append(metadata_item)
    
    return metadata_items
    

def get_manifest(opf_data, root , namespaces):
    manifest_items = []

    manifest = root.find('opf:manifest', namespaces)

    for item in manifest:
        href = item.attrib['href']
        item_id = item.attrib['id']
        media_type = item.attrib['media-type']
        properties = item.attrib.get('properties', '')
        
        item_data = {
                'href' : href,
                'item_id': item_id,
                'media_type' : media_type,
                'properties' : properties
                }

        manifest_items.append(item_data)
        #print(item_data)
    
    return manifest_items


def get_spine(opf_data, root, namespaces):
    spine_items = []
    
    spine = root.find('opf:spine', namespaces)

    for item in spine:
        if 'linear' in item.keys() :
            id_ref = item.attrib['idref']
            linear = item.attrib['linear']
            spine_item = {
                    'id_ref' : id_ref,
                    'linear' : linear
                    }
            spine_items.append(spine_item)
            #print(spine_item)
        else:
            id_ref = item.attrib['idref']    
            spine_item = {
                    'id_ref': id_ref,
                    }
            spine_items.append(spine_item)
            

def get_chapter_path(content_path, manifest):
    chapter_paths = []
    for item in manifest:
        if 'media_type' in item and item['media_type'] == 'application/xhtml+xml':
            chapter_path = content_path + item['href']
            chapter_paths.append(chapter_path)
            
    return chapter_paths

        
def get_text(chapter_urls):
    
    inner_text = ""
    for chapter_url in chapter_urls:
            
        with open(chapter_url) as chapter:
                ch_xml = chapter.read()
                root = ET.fromstring(ch_xml)
                body = root.find('.//{http://www.w3.org/1999/xhtml}body')

                if body is not None:
                    inner_text += ET.tostring(body, encoding='unicode', method='text')
                else:
                    print('no <chapter_text>')
    return inner_text


if __name__ == "__main__":
    
    #epub_path = str(input("Enter ePub path: "))
    opf_path , content_path = get_opf_path(epub_path)
    opf_data = get_opf_data(opf_path)
    root = ET.fromstring(opf_data)

    opt = int(input("Enter opertation you want to perform:\n1. Info about epub\n2. Read ePub\n"))

    match opt :
        case 1:
            res = get_metadata(opf_data, root, namespaces)
            print(res)
        case 2:
            manifest = get_manifest(opf_data, root, namespaces)
            chapter_urls = get_chapter_path(content_path, manifest)
            print(get_text(chapter_urls))
    
# func calls 
#opf_path, content_path = get_opf_path(epub_path)
#opf_data = get_opf_data(opf_path)
#root = ET.fromstring(opf_data)

#metadata = get_metadata(opf_data, root, namespaces)
#manifest = get_manifest(opf_data, root , namespaces)
#spine = get_spine(opf_data, root, namespaces)
#chapter_urls = get_chapter_path(content_path, manifest)
#get_text(chapter_urls)
#get_html(chapter_urls)



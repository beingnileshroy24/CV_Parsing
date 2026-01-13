from docx import Document
import zipfile

def inspect_xml(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        xml_content = zip_ref.read('word/document.xml').decode('utf-8')
        # Find the table part
        print(xml_content[xml_content.find('<w:tbl>'):xml_content.find('</w:tbl>')+8])

if __name__ == "__main__":
    inspect_xml('templates/tabular_template.docx')

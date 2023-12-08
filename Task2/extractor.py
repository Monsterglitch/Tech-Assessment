# Importing necessary Libraries
import PyPDF2
import pytesseract
from PIL import Image
from pdfminer.layout import LTFigure
from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages
pytesseract.pytesseract.tesseract_cmd = r"Task2\Tesseract-OCR\tesseract.exe"

# document initialization
doc_path = "Task2\sample_invoice.pdf"
doc_obj = open(doc_path, 'rb')
doc_reader = PyPDF2.PdfReader(doc_obj)

# Function to convert the PDF to image
def convert_to_images(input_file):
    images = convert_from_path(input_file, poppler_path=r"Task2\poppler-23.11.0\Library\bin")
    image = images[0]
    output_file = "./PDF_image.png"
    image.save(output_file, "PNG")

# Function to read text from image
def image_to_text(image_path):
    # Read the image
    img = Image.open(image_path)
    # Extract the text from the image
    text = pytesseract.image_to_string(img)
    return text

# Found a single LTFigure
for pagenum, page in enumerate(extract_pages(doc_path)):
    for element in page:
        pageObj = doc_reader.pages[pagenum]
        text_from_images = []
        page_content = []
        if isinstance(element, LTFigure):
            convert_to_images(doc_path)
            word = ""
            for item in image_to_text('PDF_image.png'):
                if item != ' ':
                    word += item;
                else:
                    if word:
                        text_from_images.append(word)
                        word = ""
            if word:
                text_from_images.append(word)

content = []
modified_item = ""
for item in text_from_images:
    modified_item = item.replace('\\', '').replace('\n', '').replace('\t', '')
    content.append(modified_item)

print("-"*41)
print("Invoice Date:", content[0][0:10])
print("Invoice Number: ", content[1][0:8])
print("-" * 10, "Billing Information", "-" * 10)
print("Company Name: ", content[9][4:7] + " " + content[10])
print("Name: ", content[11] + " " + content[12])
print("Address: ", content[16][7:10] + " " + content[17] + " " + content[18] + " " + content[19] + " " + content[20] + " " + content[25][4:8 ]+ " " + content[26] + " " + content[27] + " " +content[28])
print("Phone Number: ", content[33][6:12] + " " + content[34][0:8])
print("Email: ", content[34][13:29])
print("-" * 10, "Shipping Information", "-" * 10)
print("Name: ", content[13] + " " + content[14] + " " + content[15][0:5])
print("Address: ", content[21] + " " + content[22] + " " + content[23] + " " + content[24] + " " + content[25][0:4] + " " + content[29] + " " + content[30] + " " + content[31] + " " + content[32][0:5])
print("Total Invoice Amount: ", content[63])
print("Number of Items in the Invoice: ", content[57])
print("-"*41)



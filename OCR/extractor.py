# Importing necessary Libraries
import PyPDF2
# import cv2
import numpy as np
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
# print(content)

def print_section_separator():
    print("-" * 41)

def print_invoice_info(*data):
    print_section_separator()
    print("Invoice Date:", data[0][0:10])
    print("Invoice Number:", data[1][0:8])

    print_section_separator()
    print("Billing Information")
    print_section_separator()
    print("Company Name:", data[9][4:7] + " " + data[10])
    print("Name:", data[11] + " " + data[12])
    print("Address:", data[16][7:10], end=" ")
    for i in range(17, 21):
        print(data[i], end=" ")
    print(data[25][4:8] + " " + data[26] + " " + data[27] + " " + data[28])
    print("Phone Number:", data[33][6:12] + " " + data[34][0:8])
    print("Email:", data[34][13:29])

    print_section_separator()
    print("Shipping Information")
    print_section_separator()
    print("Name:", data[13] + " " + data[14] + " " + data[15][0:5])
    print("Address:", end=" ")
    for i in range(21, 26):
        print(data[25][0:4], end=" ") if i == 25 else print(data[i], end=" ")
    for i in range(29, 33):
        print(data[32][0:5]) if i == 32 else print(data[i], end=" ")

    print_section_separator()
    print("Total Invoice Amount:", data[63])
    print("Number of Items in the Invoice:", data[57])
    print_section_separator()

print_invoice_info(*content)


# image = cv2.imread("PDF_image.png")
# base_img = image.copy()
# # Grey Image
# grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("grey_image.png", grey)
# # Blurred Image
# blur = cv2.blur(grey, (10,10))
# cv2.imwrite("blur_image.png", blur)
# # Threshold Image
# thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# cv2.imwrite("threshold_image.png", thresh)
# # Kernel 
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
# # Dilated Image
# dilate = cv2.dilate(thresh, kernel, iterations=1)
# cv2.imwrite("dilated_image.png", dilate)
# # Countours
# cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# cnts = sorted(cnts, key = lambda x: cv2.boundingRect(x)[0])
# for i, c in enumerate(cnts):
#     x, y, w, h = cv2.boundingRect(c)
#     if h > 10 and w >= 100: 
#         roi = image[y:y+h, x:x+w]
#         cv2.imwrite(f"roi_image{i}.png", roi)
#     cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
# cv2.imwrite("bbox_image.png", image)
# test_img_path = 'roi_image116.png'
# test_img = np.array(Image.open(test_img_path))
# txt = pytesseract.image_to_string(test_img)
# print(txt)
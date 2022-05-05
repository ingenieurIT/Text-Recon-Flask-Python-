try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # definition
# du chemein de pytesseract


def ocr_core(filename):  # fonction qui va permettre de transformer l'image en prenant l'image en paramettre
    text = pytesseract.image_to_string(Image.open(filename))
    return text  # permet de retourner le resultat


# print(ocr_core('images/ocr_image_5.jpg'))

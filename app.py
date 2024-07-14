import os
import pytesseract
from PIL import Image
import PyPDF2
import glob
import argparse

def perform_ocr_on_image(image):
    # Perform OCR on a single image
    return pytesseract.image_to_string(image)

def process_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        # Iterate through all pages
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text

def process_file(file_path, output_folder):
    # Get the base filename
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    
    # Process based on file extension
    if ext.lower() in ['.pdf']:
        text = process_pdf(file_path)
    elif ext.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        image = Image.open(file_path)
        text = perform_ocr_on_image(image)
    else:
        print(f"Unsupported file type: {ext}")
        return
    
    # Write the result to a text file
    output_file = os.path.join(output_folder, f"{name}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Processed {base_name}")

def process_files(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process all files in the input folder
    for file_path in glob.glob(os.path.join(input_folder, '*.*')):
        process_file(file_path, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform OCR on images and PDFs.')
    parser.add_argument('--input', default='input_files', help='Input folder path')
    parser.add_argument('--output', default='output_texts', help='Output folder path')
    
    args = parser.parse_args()
    
    process_files(args.input, args.output)

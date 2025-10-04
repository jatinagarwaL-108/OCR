import streamlit as st
import pytesseract
from PIL import Image
import re
import numpy as np

st.title("Expense Extraction App with Tesseract OCR")

# If Tesseract is not in PATH, specify the executable path
# Example for Windows: pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# For Linux/Mac, Tesseract is usually in PATH by default

# File uploader
uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "jpeg"])

def extract_expense_details(text):
    """Extract amount, date, and description from text."""
    # Extract amount (last number with decimal)
    amount = re.findall(r'(\d+\.\d{2}|\d+)', text)
    amount = amount[-1] if amount else "Not found"

    # Extract date (format DD/MM/YYYY or DD-MM-YYYY)
    date = re.findall(r'(\d{2}[-/]\d{2}[-/]\d{4})', text)
    date = date[0] if date else "Not found"

    # Use first line as description
    description = text.split("\n")[0] if text else "Not found"

    return {"amount": amount, "date": date, "description": description}

if uploaded_file is not None:
    # Open image using PIL
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Receipt", use_column_width=True)

    # Convert to grayscale for better OCR accuracy (optional)
    img_gray = img.convert('L')

    # OCR using Tesseract
    extracted_text = pytesseract.image_to_string(img_gray)

    # Extract expense fields
    data = extract_expense_details(extracted_text)

    # Display extracted data
    st.subheader("Extracted Expense Data")
    st.write(f"**Amount:** {data['amount']}")
    st.write(f"**Date:** {data['date']}")
    st.write(f"**Description:** {data['description']}")

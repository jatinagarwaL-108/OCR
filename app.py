import streamlit as st
import easyocr
import re
from PIL import Image
import numpy as np

st.title("Expense Extraction App")

# Initialize EasyOCR reader (English)
reader = easyocr.Reader(['en'])

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

    # Convert PIL Image to NumPy array for EasyOCR
    img_np = np.array(img)

    # OCR using EasyOCR
    results = reader.readtext(img_np)
    extracted_text = "\n".join([res[1] for res in results])

    # Extract expense fields
    data = extract_expense_details(extracted_text)

    # Display extracted data
    st.subheader("Extracted Expense Data")
    st.write(f"**Amount:** {data['amount']}")
    st.write(f"**Date:** {data['date']}")
    st.write(f"**Description:** {data['description']}")

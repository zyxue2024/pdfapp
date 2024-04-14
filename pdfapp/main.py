"""Main page."""

from typing import List
import io

import streamlit as st
import PyPDF2
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(
    page_title="pdfapp",
    page_icon="👋",
)

st.header("Concatenating pdf files")
st.write(":blue[Just a simple utility tool for concatenating pdf files.]")


def concatenate_pdfs(pdf_files: List[UploadedFile]) -> bytes:
    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Iterate through each input PDF file
    for pdf_file in pdf_files:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    bytes_io = io.BytesIO()
    pdf_writer.write(bytes_io)
    bytes_io.seek(0)
    return bytes_io.read()


uploaded_files = st.file_uploader(
    label=(
        "Upload your pdf files to concatenate here. "
        "Note the uploaded files will be concatenated in alphabetical orders. "
        "You can prefix file name with numbers like if you'd like them to be concatenated in a particular order."
    ),
    type="pdf",
    accept_multiple_files=True,
)


if uploaded_files:
    st.write(f"Concatenating {len(uploaded_files)} pdf files in the following order:")
    sorted_files = sorted(uploaded_files, key=lambda f: f.name)
    st.markdown(
        "\n".join(
            [
                f"1. {f.name} ({len(PyPDF2.PdfReader(f).pages)} pages)"
                for f in sorted_files
            ]
        )
    )

    st.download_button(
        label="Download concatenated pdf file.",
        data=concatenate_pdfs(sorted_files),
        file_name="concatenated.pdf",
        mime="application/pdf",
    )

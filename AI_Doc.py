import streamlit as st
from pypdf import PdfReader
from docx import Document
import pymupdf4llm
import sys
import torch
import torchvision
import builtins
builtins.torch = torch
builtins.torchvision = torchvision
from transformers import pipeline
from google import genai
from openai import OpenAI
 

st.title("AI-Powered Document Extractor")
st.caption("Designed to help you process information quickly!")
 
st.subheader(":blue[Guidelines]:")
st.markdown("""
- The application supports two mode of information preprocessing; Document (PDF and docx format documents are accepted) and Text.
- Based on the document/text size you have the choice to choose the amount of words your summary to be, for your easy understanding, min. being 100 and max. being 400 words. 
""")
 
amount = st.slider("How long you want your summary to be?",100,300)
st.write(f"-> chosen limit: :green[{amount} words]")
 
def process_information():
    info_type = st.radio(
        "What kind of information you would like to summarize?",
        ["Document", "Text"]
    )

    information_processed = ""

    if info_type == "Text":
        info = st.text_area(
            "Paste your information down below!",
            placeholder="Paste..."
        )

        information_processed += info

        if not information_processed.strip():
            st.error("Currently the text is empty!")
        else:
            st.write("Extracted text:")
            st.write(information_processed)

    elif info_type == "Document":
        document = st.file_uploader(
            "Upload your file:",
            type=["pdf", "docx"]
        )

        if document is not None:
            st.markdown(f"""
                        - Name: :green[{document.name}]
                        - Type: :green[{document.type}]
""") 
            if document is not None and document.type == "application/pdf":
                st.write("Starting extraction...")
                reader = PdfReader(document)

                information_processed = ""

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        information_processed += text

                if not information_processed.strip():
                    st.warning("No extractable text found (likely scanned PDF).")
                # if st.button("Would you like ")
                st.write("Extracted PDF text:")
                st.write(information_processed[:500])

            elif document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

                docx = Document(document)

                text = "\n".join([p.text for p in docx.paragraphs])

                information_processed = text

                st.write("Extracted DOCX text:")
                st.write(information_processed)

    api_key = "API_KEY"

    # client = OpenAI(api_key=aPI_key)
    # if st.button("Summarise",icon="👍"):
    #     summary_model = pipeline("text-generation",model="facebook/bart-large-cnn")
    #     # model="facebook/bart-large-cnn"
    #     print(information_processed)
    prompt = f'''Summarize the following document, in {amount} words
    
    Document:
    {information_processed}
    
    Provide:
    1. Executive Summary
    2. Key Points
    3. Action Items'''
    #     summary = summary_model(input=prompt, max_length=300, min_length=50,do_sample=False)
    #     st.subheader("Here's the summary!")
    #     st.write(summary[0])


    client = OpenAI(
        api_key=api_key,
        base_url="BASE_URL"
    )

    response = client.chat.completions.create(
        
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    st.write("Here's the summary")
    st.write(response.choices[0].message.content)



process_information()

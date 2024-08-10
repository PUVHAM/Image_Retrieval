import os
import time
import streamlit as st
from chromadb import chromadb
from streamlit_app.chroma_client import add_embedding
from streamlit_app.chroma_search import search
from streamlit_app.directory_utils import find_path, get_files_path, change_directory
from streamlit_app.display_utils import display_results

def handle_extract(short_option):
    ROOT = 'Dataset'
    root_path = find_path(os.getcwd(), "Image_Retrieval")

    if root_path:
        if os.getcwd() != root_path:
            os.chdir(root_path)
    else:
        st.error("Cannot find the 'Image_Retrieval' directory.")
        return
    
    files_path = get_files_path(ROOT)
    chroma_client = chromadb.Client()

    with st.spinner(f'Extracting features for {short_option}...'):
        if short_option == "CS":
            if not st.session_state.extracted_cosine:
                st.session_state.collection_cosine = chroma_client.get_or_create_collection(
                    name="cosine_collection", metadata={"hwsn:space": "cosine"})
                add_embedding(collection=st.session_state.collection_cosine, files_path=files_path)
                st.session_state.extracted_cosine = True
                st.success(f'Features extracted for {short_option} successfully!')
            else:
                st.info("Cosine Similarity features already extracted.")
        else:  # L2
            if not st.session_state.extracted_l2:
                st.session_state.collection_l2 = chroma_client.get_or_create_collection(
                    name="l2_collection", metadata={"hwsn:space": "l2"})
                add_embedding(collection=st.session_state.collection_l2, files_path=files_path)
                st.session_state.extracted_l2 = True
                st.success(f'Features extracted for {short_option} successfully!')
            else:
                st.info("L2 features already extracted.")
                 
    st.session_state.files_path = files_path
    
def handle_extraction(short_option):
    if 'extract_clicked' not in st.session_state:
        st.session_state.extract_clicked = False

    extract_button = st.button("Extract")

    if extract_button:
        st.session_state.extract_clicked = True

    # Only run handle_extract if the button has been clicked
    if st.session_state.extract_clicked:
        handle_extract(short_option)
        # Reset the clicked state after extraction
        st.session_state.extract_clicked = False
    
def search_and_display_results(query_image, short_option, uploaded_file, n_results):
    collection = st.session_state.collection_cosine if short_option == "CS" else st.session_state.collection_l2
    with change_directory("src"):
        with st.spinner('Searching image...'):
            results = search(image_path=uploaded_file, collection=collection, n_results=n_results)
            time.sleep(2)
        st.success('Image uploaded successfully!') 
    
    with st.spinner('Processing results...'):
        time.sleep(2)
        display_results(query_image, results, st.session_state.files_path)
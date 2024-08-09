import streamlit as st
import os
from PIL import Image
from chromadb import chromadb
from streamlit_app.chroma_client import add_embedding
from streamlit_app.chroma_search import search
from streamlit_app.utils import get_path, display_results

def main():
    st.title("Image Retrieval App")
    
    # Choose option
    option = st.selectbox("Select similarity metric:", ("Cosine Similarity", "L2"))
        
    # Allow user to upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


    if uploaded_file is not None:
        # Display the uploaded image
        query_image = Image.open(uploaded_file)
        st.image(query_image, caption='Uploaded Image', use_column_width=True)

        # Get the number of results from the user
        n_results = st.number_input("Number of results to display", min_value=1, max_value=10, value=5, step=1)
        
        # Search button
        if st.button("Search"):
            # Perform the search
            ROOT = "Dataset"
            os.chdir(os.path.dirname(os.getcwd()))
            files_path = get_path(ROOT)
            chroma_client = chromadb.Client()
            if option == "Cosine Similarity":
                collection = chroma_client.get_or_create_collection(name="cosine_collection", 
                                                                        metadata={"hwsn:space":"cosine"}) # type: ignore
            elif option == "L2":
                collection = chroma_client.get_or_create_collection(name="l2_collection", 
                                                                        metadata={"hwsn:space":"l2"}) # type: ignore
            
            with st.spinner('Processing image...'):
                st.info("Extracting image features... This may take a while.")
                add_embedding(collection=collection, files_path=files_path)
            st.success('Complete!')
            
            results = search(image_path=uploaded_file, collection=collection, n_results=n_results)
            
            # Display the results
            display_results(query_image, results, files_path)
            os.chdir("src")


if __name__ == "__main__":
    main()
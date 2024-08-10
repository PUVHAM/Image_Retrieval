import sys
import os
from PIL import Image
import streamlit as st
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from streamlit_app.chroma_utils import search_and_display_results, handle_extraction
from streamlit_app.display_utils import display_warning_if_not_extracted

def main():
    st.set_page_config(page_title="Image Retrieval App",
                       page_icon=":night_with_stars:",
                       layout="wide",
                       menu_items={
                           'Get Help':'https://github.com/PUVHAM/Image_Retrieval',
                           'Report a Bug':'mailto:phamquangvu19082005@gmail.com',
                           'About': "# Image Retrieval App\n"
                                    "This app allows you to search and retrieve images based on content similarity."
                        }
                    )

    st.title("Image Retrieval App")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        abbreviations = {
            "Cosine Similarity": "CS",
            "L2": "L2"
        }
        option = st.selectbox("Select similarity metric:", ("Cosine Similarity", "L2"))
        
        short_option = abbreviations.get(option, option)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            on = st.toggle("Show metrics")
        with col2:
            if st.button("ℹ️", help="Click for more information about metrics"):
                st.toast("Toggling 'Show metrics' during extraction may interrupt the process. Please avoid changing it while extracting.", icon="ℹ️")
        
        st.divider()
        
        # Display warning if not extracted
        display_warning_if_not_extracted(short_option)
        handle_extraction(short_option)
        
    # Display metrics if toggled on
    if on:
        st.subheader("Similarity Metric")
        if option == "L2":
            st.latex(r"""
                \text{L2 Distance}(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}
                """)
        else:  # Cosine Similarity
            st.latex(r"""
                \text{Cosine Similarity}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \|\mathbf{b}\|}
                = \frac{\sum_{i=1}^{n} a_i b_i}{\sqrt{\sum_{i=1}^{n} a_i^2} \cdot \sqrt{\sum_{i=1}^{n} b_i^2}}
                """)
        st.divider()


    # Image upload and search section
    if (short_option == "CS" and st.session_state.extracted_cosine) or \
        (short_option == "L2" and st.session_state.extracted_l2):
            
        st.subheader("Image Search")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 2])
            with col1:
                query_image = Image.open(uploaded_file)
                st.image(query_image, caption='Uploaded Image', use_column_width=True)
            with col2:
                n_results = st.slider("Number of results to display", min_value=1, max_value=10, value=5)
                if st.button("Search", type="primary"):
                    search_and_display_results(query_image=query_image, short_option=short_option, uploaded_file=uploaded_file, n_results=n_results)

if __name__ == "__main__":
    # Initialize session state variables
    if "extracted_l2" not in st.session_state:
        st.session_state.extracted_l2 = False

    if "extracted_cosine" not in st.session_state:
        st.session_state.extracted_cosine = False

    if "collection_l2" not in st.session_state:
        st.session_state.collection_l2 = None

    if "collection_cosine" not in st.session_state:
        st.session_state.collection_cosine = None

    main()
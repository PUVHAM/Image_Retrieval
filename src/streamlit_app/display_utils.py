import os
import streamlit as st 
from PIL import Image

def process_image(image_path):
    image = Image.open(image_path).resize((448, 448))
    return image

def display_results(query_image, results, files_path):
    images = [process_image(query_image)]
    class_names = []
    for id_img in results['ids'][0]:
        id_img = int(id_img.split('_')[-1])
        img_path = files_path[id_img]
        img = process_image(img_path)
        images.append(img)
        class_names.append(os.path.basename(os.path.dirname(img_path)))
    
    st.subheader("Query Image and Top Similar Images")
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            if i == 0:
                st.image(img, caption="Query Image", use_column_width=True)
            else:
                st.image(img, caption=f"Top {i}: {class_names[i-1]}", use_column_width=True)
                
def display_warning_if_not_extracted(short_option):
    if short_option == "CS" and not st.session_state.get('extracted_cosine', False):
        st.warning("Cosine Similarity features not extracted. Please click 'Extract' to begin.")
    elif short_option == "L2" and not st.session_state.get('extracted_l2', False):
        st.warning("L2 features not extracted. Please click 'Extract' to begin.")
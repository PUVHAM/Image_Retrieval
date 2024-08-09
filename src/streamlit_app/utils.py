import os
import numpy as np
import streamlit as st
from PIL import Image
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

embedding_function = OpenCLIPEmbeddingFunction()

def get_single_image_embedding(image):
    embedding = embedding_function._encode_image(image=np.array(image))
    return embedding

def get_path(root_dir):
    files_path = []
    for class_dir in os.listdir(root_dir):
        class_path = os.path.join(root_dir, class_dir)
        if os.path.isdir(class_path):
            for feature_dir in os.listdir(class_path):
                feature_path = os.path.join(class_path, feature_dir)
                if os.path.isdir(feature_path):
                    for filename in os.listdir(feature_path):
                        file_path = os.path.join(feature_path, filename)
                        files_path.append(file_path)
    return files_path

def display_results(query_image, results, files_path):
    images = [query_image.resize((448, 448))]
    class_names = []
    for id_img in results['ids'][0]:
        id_img = int(id_img.split('_')[-1])
        img_path = files_path[id_img]
        img = Image.open(img_path).resize((448, 448))
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
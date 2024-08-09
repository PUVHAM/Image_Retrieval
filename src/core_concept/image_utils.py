import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

embedding_function = OpenCLIPEmbeddingFunction()

def get_single_image_embedding(image):
    embedding = embedding_function._encode_image(image)
    return np.array(embedding)

def read_image_from_path(path, size):
    img = Image.open(path).convert('RGB').resize(size)
    return np.array(img)

def folder_to_images(folder, size):
    list_dir = [folder + '/' + name for name in os.listdir(folder)]
    images_np = np.zeros(shape=(len(list_dir), *size, 3))
    images_path = []
    
    for i, path in enumerate(list_dir):
        images_np[i] = read_image_from_path(path, size)
        images_path.append(path)
    images_path = np.array(images_path)
    return images_np, images_path

def plot_results(query_path, lst_path_score, reverse=False, top_k=5):
    lst_path_score.sort(key=lambda x: x[1], reverse=reverse)
    top_results = lst_path_score[:top_k]
    
    fig = plt.figure(figsize=(15, 9))
    ax1 = fig.add_subplot(2, top_k + 1, 1)
    query_img = Image.open(query_path).resize((448, 448))
    ax1.imshow(query_img)
    ax1.set_title(f"Query Image: \n{os.path.basename(os.path.dirname(query_path))}", fontsize=16)
    ax1.axis("off")   
    
    for i, (path, score) in enumerate(top_results):
        ax = fig.add_subplot(2, top_k + 1, i + 2)
        img = Image.open(path).resize((448, 448))
        ax.imshow(img)
        ax.set_title(f'Score: {score:.2f}\n Top {i + 1}: \n{os.path.basename(os.path.dirname(path))}', fontsize=16)
        ax.axis("off")
    
    plt.show()
    
def plot_results_st(query_path, lst_path_score, reverse=False, top_k=5):
    lst_path_score.sort(key=lambda x: x[1], reverse=reverse)
    top_results = lst_path_score[:top_k]
    
    query_img = Image.open(query_path).resize((448, 448))
    
    num_cols = 3  # Số cột muốn hiển thị, bạn có thể điều chỉnh theo ý muốn
    rows = (top_k + 1) // num_cols + ((top_k + 1) % num_cols > 0)

    for row in range(rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            idx = row * num_cols + col
            if idx == 0:
                with cols[col]:
                    st.image(query_img, caption=f'Query Image: {os.path.basename(os.path.dirname(query_path))}', use_column_width=True)
            elif idx <= top_k:
                img_path, score = top_results[idx - 1]
                img = Image.open(img_path).resize((448, 448))
                with cols[col]:
                    st.image(img, caption=f'Score: {score:.2f}\n Top {idx}: {os.path.basename(os.path.dirname(img_path))}', use_column_width=True)
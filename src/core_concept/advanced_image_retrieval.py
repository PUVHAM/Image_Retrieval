import os
import numpy as np
from metrics import SimilarityMetrics
from image_utils import read_image_from_path, get_single_image_embedding, folder_to_images, plot_results
from config import ROOT, CLASS_NAME

def get_l1_score(root_img_path, query_path, size):
    query = read_image_from_path(query_path, size)
    query_embedding = get_single_image_embedding(query)
    lst_path_score = []
    for folder in os.listdir(root_img_path):
        if folder in CLASS_NAME:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path, size)
            embedding_lst = []
            for idx_img in range(images_np.shape[0]):
                embedding = get_single_image_embedding(images_np[idx_img].astype(np.uint8))
                embedding_lst.append(embedding)
            rates = SimilarityMetrics(query_embedding, np.stack(embedding_lst)).absolute_difference()
            lst_path_score.extend(list(zip(images_path, rates)))
    return query, lst_path_score

def get_l2_score(root_img_path, query_path, size):
    query = read_image_from_path(query_path, size)
    query_embedding = get_single_image_embedding(query)
    lst_path_score = []
    for folder in os.listdir(root_img_path):
        if folder in CLASS_NAME:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path, size)
            embedding_lst = []
            for idx_img in range(images_np.shape[0]):
                embedding = get_single_image_embedding(images_np[idx_img].astype(np.uint8))
                embedding_lst.append(embedding)
            rates = SimilarityMetrics(query_embedding, np.stack(embedding_lst)).mean_square_difference()
            lst_path_score.extend(list(zip(images_path, rates)))
    return query, lst_path_score

def get_cosine_similarity_score(root_img_path, query_path, size):
    query = read_image_from_path(query_path, size)
    query_embedding = get_single_image_embedding(query)
    lst_path_score = []
    for folder in os.listdir(root_img_path):
        if folder in CLASS_NAME:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path, size)
            embedding_lst = []
            for idx_img in range(images_np.shape[0]):
                embedding = get_single_image_embedding(images_np[idx_img].astype(np.uint8))
                embedding_lst.append(embedding)
            rates = SimilarityMetrics(query_embedding, np.stack(embedding_lst)).cosine_similarity()
            lst_path_score.extend(list(zip(images_path, rates)))
    return query, lst_path_score

def get_correlation_coefficient_score(root_img_path, query_path, size):
    query = read_image_from_path(query_path, size)
    query_embedding = get_single_image_embedding(query)
    lst_path_score = []
    for folder in os.listdir(root_img_path):
        if folder in CLASS_NAME:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path, size)
            embedding_lst = []
            for idx_img in range(images_np.shape[0]):
                embedding = get_single_image_embedding(images_np[idx_img].astype(np.uint8))
                embedding_lst.append(embedding)
            rates = SimilarityMetrics(query_embedding, np.stack(embedding_lst)).correlation_coefficient()
            lst_path_score.extend(list(zip(images_path, rates)))
    return query, lst_path_score

if __name__ == "__main__":
    root_img_path = f"{ROOT}/train/"
    query_path = f"{ROOT}/test/Orange_easy/0_100.jpg"
    size = (448, 448)
    query, lst_path_score = get_l2_score(root_img_path, query_path, size)
    plot_results(query_path, lst_path_score, reverse=False)

    root_img_path = f"{ROOT}/train/"
    query_path = f"{ROOT}/test/African_crocodile/n01697457_18534.JPEG"
    size = (448, 448)
    query, lst_path_score = get_cosine_similarity_score(root_img_path, query_path, size)
    plot_results(query_path, lst_path_score, reverse=True)
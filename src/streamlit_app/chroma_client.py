from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def add_embedding(collection, files_path):
    from streamlit_app.image_utils import process_image

    ids = []
    embeddings = []
    
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_image, files_path), total=len(files_path)))

    for id_filepath, embedding in enumerate(results):
        ids.append(f'id_{id_filepath}')
        embeddings.append(embedding)
    collection.add(
        embeddings=embeddings,
        ids=ids
    )
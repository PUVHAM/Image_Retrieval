from PIL import Image

def search(image_path, collection, n_results):
    from streamlit_app.image_utils import get_single_image_embedding
    query_image = Image.open(image_path)
    query_embedding = get_single_image_embedding(query_image)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results
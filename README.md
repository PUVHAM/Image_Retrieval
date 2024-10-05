# Image Retrieval Project

This repository contains code and instructions for an image retrieval system using basic mathematical methods and advanced techniques. The project provides a user-friendly interface through Streamlit for users to interact with the model and utilizes ChromaDB for efficient vector storage and retrieval.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1vehgkbYusOfYISu-HRjsbu1ZlFSgKvFa" width="470" height="295" style="margin-right: 5%;" />
  <img src="https://drive.google.com/uc?export=view&id=1AKdxsK5ik1paGlfwmR1v416pONerJgrc" width="470" height="295" />
</p>

## Table of Contents
- [Purpose](#purpose)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Streamlit App](#running-the-streamlit-app)
  - [Running with Docker](#running-with-docker)
  - [Using the Streamlit App](#using-the-streamlit-app)
  - [Data Crawling](#data-crawling)
- [Model and Dataset](#model-and-dataset)
- [Acknowledgments](#acknowledgments)

## Purpose

The purpose of this project is to demonstrate image retrieval techniques using both basic mathematics and advanced methods. It showcases the use of similarity metrics such as L2 distance and Cosine similarity, as well as feature extraction using the CLIP model. The system allows users to upload an image and find similar images from a dataset.

## Key Features

- Image retrieval using basic mathematics (L1, L2, cosine similarity, correlation coefficient)
- Advanced feature extraction using the CLIP model
- Intuitive user interface with Streamlit
- Efficient vector storage and retrieval using ChromaDB
- Multi-threading for optimized feature extraction process
- Support for custom dataset crawling and preparation

## Project Structure

- **Dataset/**: Contains the image dataset used for retrieval.
- **src/core_concept/**: Basic and advanced image retrieval implementations.
- **src/crawl_data/**: Scripts for data crawling and cleaning.
- **src/streamlit_app/**: Optimized image retrieval using CLIP and ChromaDB.
- **app.py**: Main Streamlit application file.
- **requirements.txt**: List of project dependencies.

## Installation

To get started, clone the repository and install the required dependencies.

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)

### Step-by-Step Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/PUVHAM/Image_Retrieval.git
    cd Image_Retrieval
    ```

2. **Create and Activate Conda Environment:**

    ```bash
    conda create --name image_retrieval python=3.11
    conda activate image_retrieval
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    This will install necessary Python packages including Streamlit, ChromaDB, and other dependencies.

## Usage 

### Running the Streamlit App

The Streamlit app allows users to upload images and search for similar images in the dataset.
1. **Navigate to the `src` directory:**

   ```bash
    cd src
    ```

2. **Start the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

### Running with Docker

#### Prerequisites
  - [Docker](https://www.docker.com/get-started): Make sure Docker is installed on your system.
1. **Build docker image:**
     
    ```bash
    docker build -t image_retrieval -f docker/Dockerfile .
    ```
    
2. **Run a docker container:**
   
    ```bash
    docker run -d -p 8501:8501 -it --name image_retrieval image_retrieval
    ```
3. **Access the Streamlit App:**
  - Once the Docker container is running, open your web browser and go to:

    ```bash
    http://localhost:8501
    ```
    
    You should see the Image Retrieval Streamlit app interface, where you can interact with the model by uploading images, selecting similarity metrics, and viewing results.

### Using the Streamlit App
   - Select the similarity metric (Cosine Similarity or L2) from the sidebar.
   - Click the "Extract" button to extract features from the dataset and store them in ChromaDB (only needs to be done once for each method).
   - Upload an image to search for similar images.
   - Adjust the number of results you want to display.
   - Click "Search" to view similar images.

### Data Crawling

The project includes scripts for crawling and cleaning data from Flickr. To use these scripts:

1. **Navigate to the `src/crawl_data` directory:**

    ```bash
    cd src/crawl_data
    ```
    
2. **Run the scripts in the following order:**

    ```bash
    python crawl_url.py
    python crawl_img.py
    python clean_dataset.py
    ```
    
    This will create and populate the `Dataset` folder with crawled and cleaned images.
   
3. **Organize data:**

     ```bash
    python organize_folder.py
    ```

    The `organize_folder.py` will organize the `Dataset` folder into a `data` directory with two subfolders: `train` and `test`.


## Model and Dataset
- The project uses both basic mathematical models and the CLIP model for feature extraction.
- A subset of ImageNet1K is used as a sample dataset (`src/core_concept/core_data`).
- Users can crawl and use their own datasets using the provided scripts.

## Acknowledgments

- [CLIP Model](https://github.com/openai/CLIP) for advanced feature extraction
- [Streamlit](https://streamlit.io/) for the user interface
- [ChromaDB](https://www.trychroma.com/) for integrating CLIP model and efficient vector storage and retrieval
- [Flickr](https://flickr.com/) for the image dataset

Feel free to reach out if you have any questions or issues!

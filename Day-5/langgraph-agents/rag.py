from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import numpy as np
import chromadb

chroma_client = chromadb.PersistentClient("db")
collection_name='products'

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding

def rag(query: str) -> str:

    collection = chroma_client.get_collection(name=collection_name)
    query_embedding = get_embedding(query)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # Perform vector search
    search_results = collection.query(
        query_embeddings=query_embedding, 
        n_results=3 
    )

    metadatas = search_results.get('metadatas', [])

    search_result = ""
    i = 0

    for i, metadata_list in enumerate(metadatas):
        if isinstance(metadata_list, list):  # Ensure it's a list
            for metadata in metadata_list:  # Iterate through all dicts in the list
                if isinstance(metadata, dict):
                    combined_text = metadata.get('information', 'No text available').strip()

                    search_result += f"{i}). \n{combined_text}\n\n"
                    i += 1
    return search_result


def shop_information_rag():
    return [
        {
        "address": "89 Đ. Tam Trinh, Mai Động, Hoàng Mai, Hà Nội 100000, Vietnam",
        "maps_url": "https://maps.app.goo.gl/SitTbiYwUpu8jpeRA",
        "opening_hours": "8:30 AM–9:30 PM"
        },
        {
        "address": "27A Nguyễn Công Trứ, Phạm Đình Hổ, Hai Bà Trưng, Hà Nội 100000, Vietnam",
        "maps_url": "https://maps.app.goo.gl/3L7iSHpbHawsEaTx9",
        "opening_hours": "8:30 AM–9:30 PM"
        },
        {
        "address": "392 Đ. Trương Định, Tương Mai, Hoàng Mai, Hà Nội, Vietnam",
        "maps_url": "https://maps.app.goo.gl/torAE2bHddW6nMPq9",
        "opening_hours": "8:30 AM–9:30 PM"
        }
    ]

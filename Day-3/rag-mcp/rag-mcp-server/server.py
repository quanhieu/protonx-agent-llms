from dotenv import load_dotenv
import chromadb
import os
import numpy as np
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

chroma_client = chromadb.PersistentClient("db")
collection_name='products'

load_dotenv()

@mcp.tool()
def rag(query: str) -> str:

    collection = chroma_client.get_collection(name=collection_name)
    query_embedding = get_embedding(query)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # Perform vector search
    search_results = collection.query(
        query_embeddings=query_embedding, 
        n_results=10
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


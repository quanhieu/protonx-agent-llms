from mcp.server.fastmcp import FastMCP
import sqlite3
mcp = FastMCP("My App")
from typing import List, Dict, Any, Optional
from create_mock_db import create_mock_database
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import numpy as np

chroma_client = chromadb.PersistentClient("C:\\Users\\Admin\\Desktop\\protonx-agent-01-class\\Day-4\\resource-demo\\db")
collection_name='products'

collections = chroma_client.list_collections()
print(collections)

load_dotenv()
create_mock_database()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding

import pandas as pd

@mcp.tool(
    name="RAG",
    description=
        f"Use this tool to answer questions about the phone data. You can use this tool multiple times if needed.\n" 
        f"Use this tool when user ask about the phone data, product data, price, color, etc.",
)
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

@mcp.resource("file:///data/hoanghamobile.csv", name="Mobile Phone Data", mime_type="application/json")
def get_mobile_data() -> str:
    """Return mobile phone product data from hoanghamobile.csv as JSON"""
    try:
        # Get the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the CSV file
        csv_path = os.path.join(script_dir, "hoanghamobile.csv")

        # Read the CSV file using pandas
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Convert DataFrame to a list of dictionaries
        records = df.to_dict(orient='records')
        
        # Return as JSON string
        return json.dumps({"products": records}, indent=2, default=str)
    except Exception as e:
        # Handle any errors
        return json.dumps({"error": f"Failed to read CSV data: {str(e)}"}, indent=2)


@mcp.resource("file:///docs/readme.md", name="README", mime_type="text/markdown")
def get_readme() -> str:
    """Sample README file for the application"""
    return """# My Application. This is a sample README file for the application."""

@mcp.resource("file:///logs/app.log", name="Application Logs", mime_type="text/plain")
def get_logs() -> str:
    """Sample application logs"""
    return "2025-04-15 12:00:00 INFO Starting application\n2025-04-15 12:00:05 INFO Connected to database\n2025-04-15 12:01:10 WARN High memory usage detected"

@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect("database.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.resource("api://users", name="User List", mime_type="application/json")
def get_users() -> str:
    """Return all users from the database as JSON"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    # Query to get all users (excluding sensitive data like password_hash)
    cursor.execute("""
        SELECT id, username, email, created_at, last_login 
        FROM users
    """)
    
    # Convert the result to a list of dictionaries
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Return as JSON string
    return json.dumps({"users": users}, indent=2, default=str)


@mcp.resource("api://users/{user_id}", name="User by ID", mime_type="application/json")
def get_user_by_id(user_id: str) -> str:
    """Return a specific user by ID"""
    try:
        # Validate that user_id is an integer
        user_id_int = int(user_id)
        
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query to get a specific user by ID
        cursor.execute("""
            SELECT id, username, email, created_at, last_login 
            FROM users 
            WHERE id = ?
        """, (user_id_int,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # User found, return as JSON
            return json.dumps({"user": dict(user)}, indent=2, default=str)
        else:
            # User not found
            return json.dumps({"error": f"User with ID {user_id} not found"}, indent=2)
            
    except ValueError:
        # Invalid user ID format
        return json.dumps({"error": "Invalid user ID format. User ID must be an integer."}, indent=2)

@mcp.tool("get_weather", "Get the weather for a specific location")
def get_weather(location: str) -> str:
    """Return the weather for the user's location"""
    



# Add this at the end of your file
if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
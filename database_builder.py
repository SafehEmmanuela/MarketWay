import sqlite3
import json
import os
import pickle
import numpy as np

# Configuration
DB_PATH = "market.db"
DATA_PATH = "data/market_data.json"
MODEL_NAME = "all-MiniLM-L6-v2"

def get_embedding_model():
    """
    Returns a function that takes text and returns an embedding.
    Tries to load sentence-transformers, falls back to random if not available.
    """
    try:
        from sentence_transformers import SentenceTransformer
        print(f"Loading {MODEL_NAME}...")
        model = SentenceTransformer(MODEL_NAME)
        return model.encode
    except Exception as e:
        print(f"WARNING: sentence-transformers failed to load ({e}). Using dummy embeddings.")
        # Return a dummy function that returns a random vector of size 384 (MiniLM default)
        return lambda text: np.random.rand(384).astype(np.float32)

def create_schema(cursor):
    print("Creating schema...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lines (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price REAL,
        line_id INTEGER,
        FOREIGN KEY(line_id) REFERENCES lines(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT, -- 'line' or 'product'
        entity_id INTEGER,
        embedding BLOB
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        target_id INTEGER,
        distance REAL,
        direction TEXT,
        FOREIGN KEY(source_id) REFERENCES lines(id),
        FOREIGN KEY(target_id) REFERENCES lines(id)
    )
    """)

def load_data(cursor, data_path, embed_func):
    print(f"Loading data from {data_path}...")
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Insert Lines
    for line in data.get("lines", []):
        cursor.execute("INSERT OR REPLACE INTO lines (id, name, description) VALUES (?, ?, ?)",
                       (line['id'], line['name'], line['description']))
        
        # Generate embedding for line
        text = f"{line['name']}: {line['description']}"
        embedding = embed_func(text)
        blob = pickle.dumps(embedding)
        cursor.execute("INSERT INTO embeddings (entity_type, entity_id, embedding) VALUES (?, ?, ?)",
                       ('line', line['id'], blob))

    # Insert Products
    for product in data.get("products", []):
        cursor.execute("INSERT OR REPLACE INTO products (id, name, description, price, line_id) VALUES (?, ?, ?, ?, ?)",
                       (product['id'], product['name'], product['description'], product['price'], product['line_id']))
        
        # Generate embedding for product
        text = f"{product['name']}: {product['description']}"
        embedding = embed_func(text)
        blob = pickle.dumps(embedding)
        cursor.execute("INSERT INTO embeddings (entity_type, entity_id, embedding) VALUES (?, ?, ?)",
                       ('product', product['id'], blob))

    # Insert Connections
    for conn in data.get("connections", []):
        # Insert both directions for undirected graph behavior if needed, 
        # but usually we store edges. Let's store as directed edges for now.
        cursor.execute("INSERT INTO connections (source_id, target_id, distance, direction) VALUES (?, ?, ?, ?)",
                       (conn['source'], conn['target'], conn['distance'], conn['direction']))
        
        # Optional: Insert reverse edge if the graph is undirected
        # reverse_dir = f"Reverse of {conn['direction']}" # Simplified
        # cursor.execute("INSERT INTO connections (source_id, target_id, distance, direction) VALUES (?, ?, ?, ?)",
        #                (conn['target'], conn['source'], conn['distance'], reverse_dir))

    print("Data loaded and embeddings generated.")

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Start fresh for this build script
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_schema(cursor)
    
    embed_func = get_embedding_model()
    
    load_data(cursor, DATA_PATH, embed_func)
    
    conn.commit()
    conn.close()
    print(f"Database built at {DB_PATH}")

if __name__ == "__main__":
    main()
print("Database built successfully.")
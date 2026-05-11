
import chromadb
import os

db_path = os.path.join(os.getcwd(), "tru", "chroma_db")
client = chromadb.PersistentClient(path=db_path)

try:
    client.delete_collection("anti_gravity_memory")
    print("Successfully deleted 'anti_gravity_memory' collection.")
except Exception as e:
    print(f"Error: {e}")

# Re-create it fresh
client.create_collection("anti_gravity_memory")
print("Successfully re-created fresh 'anti_gravity_memory' collection.")

import json
import chromadb


def load_data_to_chromadb(data, client, collection_name):
    collection = client.get_or_create_collection(name=collection_name)

    ids = [f"doc{i+1}" for i in range(len(data))]
    metadatas_to_add = [{'association': item['association'], 'source': item['source']} for item in data]
    documents_to_add = [item['content'] for item in data]
  
    collection.add(
        metadatas=metadatas_to_add,
        documents=documents_to_add,
        ids=ids
    )
    return collection

def is_chromadb_empty(client):
    collection_names = client.list_collections()
    return not bool(collection_names) # Returns True if empty, False, if not empty


def display_data_in_chromadb(client):
    
    collection_names = client.list_collections()
    
    if collection_names:
        print(f"Collections:\n{collection_names}")
        for collection_name in collection_names:
            print(f"\nData in collection '{collection_name}':")
            try:
                collection = client.get_collection(name=collection_name)
                collection_data = collection.get()
                print(f'Collection: {collection_name}\n\nCollection Data:\n{collection_data}\n\n')
            except Exception as e:
                print(f"Error retrieving data from collection '{collection_name}': {e}")
        

def get_sample_query_result(query, collection):
    
    results = collection.query(
    query_texts=[query], # ChromaDB will embed this for you
    n_results=2 # number of results to return
    )
    
    return results


def main():
    
    # Variables
    rag_path = "rag_collection"
    input_jsonl_file = f'{rag_path}/rag_cardiovascular_disease_risk.jsonl'
    chromadb_host = "localhost"
    chromadb_port = 8001
    collection_name = "cardiovascular_disease_risk_screening_explanation"
    
    data = []
    print(f"Loading data from: {input_jsonl_file} in load_check_chromadb.py")
    with open(input_jsonl_file, 'r') as file:
        for line in file:
            json_object = json.loads(line)  # Parse each line as a JSON object
            data.append(json_object)
 
    print(f"Connecting to ChromaDB at {chromadb_host}:{chromadb_port} in load_check_chromadb.py")
    client = chromadb.HttpClient(host=chromadb_host, port=chromadb_port)
    print(f"Connected to ChromaDB at {chromadb_host}:{chromadb_port} in load_check_chromadb.py")
    
    # Check data in chromadb container before loading
    # Display initial state
    #display_data_in_chromadb(client)
    
    if is_chromadb_empty(client): # Check if ChromaDB is empty
        print(f"Status of ChromaDB: ChromaDB is empty")
        print(f"Loading data into ChromaDB collection: '{collection_name}'")
        collection = load_data_to_chromadb(data, client, collection_name)
        print(f"\nSuccessfully added {collection.count()} documents to ChromaDB collection '{collection_name}'.\n\n")
        display_data_in_chromadb(client)
    else:
        print(f"Status of ChromaDB: ChromaDB is not empty")
        print(f"Skipping data loading for collection '{collection_name}'.")
        display_data_in_chromadb(client)
    
    '''
    # Query ChromaDB
    
    # Get collection "cardiovascular_disease_risk_screening_explanation"
    collection = client.get_collection(name=collection_name)
    
    query = "A 50-year-old male with a height of 168 cm and weight of 62.0 kg has a systolic blood pressure of 110 mm Hg and diastolic blood pressure of 80 mm Hg. His cholesterol level is normal, and glucose is normal. He does not smoke, does not consume alcohol, and is physically active."
        
    results = get_sample_query_result(query, collection)
    print(f"Query:\n{query}\n\nResults:\n{results}\n\n")
    
    
    sentence_pairs = []

    if results and 'documents' in results and 'metadatas' in results and results['documents'] and results['metadatas']:
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]

        for i in range(len(documents)):
            document = documents[i]
            source = metadatas[i]['source']
            sentence_pairs.append({'document': document, 'source': source})
    
    print("Documents with Sources:\n")
    print(sentence_pairs)
    '''
if __name__ == "__main__":
    main()
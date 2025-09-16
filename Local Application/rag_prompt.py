import chromadb
import load_check_chromadb
import llm

# Variables
chromadb_host = "localhost"
chromadb_port = 8001
collection_name = "cardiovascular_disease_risk_screening_explanation"
instruction_string = "What is the screening result for this patient's cardiovascular disease risk?"


# Functions
def get_query_result(query, collection):
    
    results = collection.query(
    query_texts=[query], # Chroma will embed this for you
    n_results=2 # how many results to return
    )
    
    return results

def get_document_source(results):
    
    document_source_pairs = []

    if results and 'documents' in results and 'metadatas' in results and results['documents'] and results['metadatas']:
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]

        for i in range(len(documents)):
            document = documents[i]
            source = metadatas[i]['source']
            document_source_pairs.append(f'{document} ({source})')
            
    return document_source_pairs


def create_prompt(query: str):
    
    print(f"Patient Case Data in rag_prompt.py:\n{query}\n")
    
    print(f"Instruction String in rag_prompt.py:\n{instruction_string}\n")   
    
    prompt = f"{query} {instruction_string}"
    
    print(f"Prompt in rag_prompt.py:\n{prompt}\n")
     
    received_llm_response = llm.process_prompt(prompt)
    
    print(f"Received LLM Response in rag_prompt.py:\n{received_llm_response}\n")
    
    # Call main function from load_check_chromadb.py
    load_check_chromadb.main() 
    
    # Create connection with ChromaDB
    print(f"Connecting to ChromaDB at {chromadb_host}:{chromadb_port} in rag_prompt.py")
    client = chromadb.HttpClient(host=chromadb_host, port=chromadb_port)
    print(f"Connected to ChromaDB at {chromadb_host}:{chromadb_port} in rag_prompt.py")
    
    # Get collection "cardiovascular_disease_risk_screening_explanation" from ChromaDB
    collection = client.get_collection(name=collection_name)
    
    results = get_query_result(query, collection)
    
    print(f"Results in rag_prompt.py:\n{results}\n")
    
    document_source_pairs = get_document_source(results)
    
    print(f"Document Source Pairs in rag_prompt.py:\n{document_source_pairs}\n")
    
    rag_retrieved_similar_text = ''
    document_source_text = ''
    starting_relevant_info_text = f"Relevant Information:\n"
    
    i=0
    for document_source_pair in document_source_pairs:
        document_source_text = document_source_text + f"{i+1}. {document_source_pair}\n"
        i=i+1
    
    rag_retrieved_similar_text = starting_relevant_info_text + document_source_text
    
    print(f"RAG Retrieved Similar Text in rag_prompt.py:\n{rag_retrieved_similar_text}\n")
    
    display_response = f"{received_llm_response}\n\n{rag_retrieved_similar_text}"
    
    print(f"Display Response in rag_prompt.py:\n{display_response}\n")
    
    return display_response
    

#def main():
    
    
    #create_prompt('A 85-year-old male with a height of 178 cm and weight of 65.0 kg has a systolic blood pressure of 130 mm Hg and diastolic blood pressure of 90 mm Hg. His cholesterol level is above normal, and glucose is above normal. He smokes, consumes alcohol, and is not physically active.')
    
    #create_prompt('A 25-year-old male with a height of 178 cm and weight of 65.0 kg has a systolic blood pressure of 110 mm Hg and diastolic blood pressure of 80 mm Hg. His cholesterol level is normal, and glucose is normal. He does not smoke, does not consume alcohol, and is physically active.')


#if __name__ == "__main__":
#    main()
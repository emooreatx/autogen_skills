from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import logging
import sys
import os

def setup_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

def index_and_query(documents_dir, persist_dir, query_text):
    setup_logging()
    try:
        if not os.path.exists(persist_dir):
            logging.info("Persist directory does not exist. Creating and persisting index.")
            documents = SimpleDirectoryReader(documents_dir).load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=persist_dir)
        else:
            logging.info("Persist directory exists. Loading index.")
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
        
        if index is not None:
            query_engine = index.as_query_engine()
            response = query_engine.query(query_text)
        if response is not None:
            print("Response object type:", type(response))
            print("Response object attributes:", dir(response))
        if hasattr(response, 'response'):
            print("Query Response:")
            print(response.response)
    else:
        print("The response object does not have a 'response' attribute.")
else:
    print("No response received from the query.")
        else:
            logging.error("Failed to create or load index.")
            return None
    except Exception as e:
        logging.error(f"Error during indexing or querying: {e}")
        return None
response = index_and_query(documents_dir, persist_dir, query_text)

# Check if the response is not None and print the contents of the 'response' attribute

if __name__ == "__main__":
    DOCUMENTS_DIR = "/home/emoore/ccmp_ai/docs/bitsavers_sel_810"
    PERSIST_DIR = "/home/emoore/ccmp_ai/storage"
    query_text = "what was the cycle time for the SEL 810A?"

    response = index_and_query(DOCUMENTS_DIR, PERSIST_DIR, query_text)
    if response is not None:
        print(response)
    else:
        logging.error("No response received from the query.")

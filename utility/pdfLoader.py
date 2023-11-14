# from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone
# from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

# Initialize the sentence transformer model
# modelPath = '.venv\\.cache\\torch\\sentence_transformers\\microsoft_deberta-v2-xlarge'

# model = SentenceTransformer(modelPath)


def create_docsearch(html_path, openai_api_key, pinecone_api_key, index_name):
    # Read the HTML file and parse it using BeautifulSoup
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all <div> elements and extract their content, class, and id attributes
    div_elements = soup.find_all('div')
    documents = []

    for div in div_elements:
        content = div.get_text()
        div_class = ' '.join(div.get('class', []))
        div_id = div.get('id', None)


        print(div_class)

        # Create a dictionary with content, class, and id as metadata
        metadata = {'class': div_class, 'id': div_id}
        document = {'content': content, 'metadata': metadata}
        documents.append(document)

    print(f'You have {len(documents)} chunks in your data')

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    print('oi1')
    pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
    print('oi2')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
        # Use the 'content' key to create the 'texts' list
        texts = [d['content'] for d in documents]
        # Include the 'metadata' key to pass class and id attributes as metadata
        metadata_list = [d['metadata'] for d in documents]
        docsearch = Pinecone.from_texts(texts, embeddings, index_name=index_name, metadatas=metadata_list)
    else:
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
    
    print('oi3')
    return docsearch

# Function to vectorize text
# def vectorize(text):
#     return model.encode(text).tolist()

# def search_pdf(query, index_name):

#     index = pinecone.Index(index_name=index_name)
#     vector = vectorize(query)
#     print(vector)
#     result = index.query(vector=[vector], top_k=10,include_metadata=True)
#     print(result)
#     # match_id = result['results'][0]['matches'][0]['id']
#     location = result['matches'][0]['metadata']['text']
#     return location
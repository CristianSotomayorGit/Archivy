from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
modelPath = '.venv\\.cache\\torch\\sentence_transformers\\microsoft_deberta-v2-xlarge'

model = SentenceTransformer(modelPath)

def create_docsearch(pdf_path, openai_api_key, pinecone_api_key, index_name):

    loader = UnstructuredPDFLoader(pdf_path)
    data = loader.load_and_split()

    print(f'You have {len(data)} documents in your data')
    print(f'There are {len(data[0].page_content)}')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    print(f'Now you have {len(texts)} documents')

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    print('oi1')
    pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
    print('oi2')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
        docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    else:
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
    
    print('oi3')
    return docsearch

# Function to vectorize text
def vectorize(text):
    return model.encode(text).tolist()

def search_pdf(query, index_name):

    index = pinecone.Index(index_name=index_name)
    vector = vectorize(query)
    print(vector)
    result = index.query(vector=[vector], top_k=10,include_metadata=True)
    print(result)
    # match_id = result['results'][0]['matches'][0]['id']
    location = result['matches'][0]['metadata']['text']
    return location
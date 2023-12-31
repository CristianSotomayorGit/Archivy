from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone
from bs4 import BeautifulSoup

def create_docsearch(html_path, openai_api_key, pinecone_api_key, index_name):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    div_elements = soup.find_all('div')
    documents = []

    for div in div_elements:
        content = div.get_text()
        div_class = ' '.join(div.get('class', []))
        div_id = div.get('id', None)

        metadata = {'class': div_class, 'id': div_id}
        document = {'content': content, 'metadata': metadata}
        documents.append(document)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
        texts = [d['content'] for d in documents]
        metadata_list = [d['metadata'] for d in documents]
        docsearch = Pinecone.from_texts(texts, embeddings, index_name=index_name, metadatas=metadata_list)
    else:
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
    
    return docsearch
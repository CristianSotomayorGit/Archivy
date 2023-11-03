from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import t
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone

import unstructured
from langchain.embeddings import OpenAIEmbeddings
import pinecone
import openai

def create_docsearch(pdf_path, openai_api_key, pinecone_api_key, index_name):
    """
    Creates a docsearch using provided parameters.

    Parameters:
    - pdf_path (str): Path to the PDF document.
    - openai_api_key (str): API key for OpenAI.
    - pinecone_api_key (str): API key for Pinecone.
    - index_name (str): Name for the Pinecone index.

    Returns:
    - tuple: The docsearch object and the Pinecone index.
    """

    # Configure OpenAI
    openai.api_key = openai_api_key

    # Initialize Pinecone
    pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=4096)  # Adjust dimension as needed
    index = pinecone.Index(index_name=index_name)

    # Load PDF document and partition it by pages
    doc = unstructured.load_document(pdf_path)
    pages = unstructured.partition_pdf(doc, include_page_breaks=True)

    # Index the content of each page
    for i, page in enumerate(pages, start=1):
        text_content = page.text
        vector = openai.Embed.create(model="text-similarity-ada-001", input_texts=[text_content])['data'][0]['embedding']
        metadata = {'location': {'page': i, 'content': text_content}}
        index.upsert(ids=[f"{i}"], vectors=[vector], metadata=[metadata])

    print('Document indexed successfully.')

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Creating a dummy docsearch object for demonstration purposes
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

    return docsearch, index
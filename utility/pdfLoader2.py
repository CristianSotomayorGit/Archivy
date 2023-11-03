import pdfplumber
from sentence_transformers import SentenceTransformer
import pinecone

# Initialize Pinecone and create an index
# pinecone.init(api_key='your-pinecone-api-key', environment='us-west1-gcp')
# index_name = 'pdf-index'
# pinecone.create_index(index_name, dimension=384)
# index = pinecone.Index(index_name=index_name)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to vectorize text
def vectorize(text):
    return model.encode(text).tolist()

# Preprocess PDF and index the vectors with location information
def create_searchable_index(pdf_path,pinecone_api_key):
    print(pdf_path)
    # Initialize Pinecone and create an index
    pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
    index_name = 'langchain1'
    # pinecone.create_index(index_name, dimension=384)
    index = pinecone.Index(index_name=index_name)
    
    # with pdfplumber.open(pdf_path) as pdf:
    #     for page_num, page in enumerate(pdf.pages):
    #         text = page.extract_text()
    #         for i, paragraph in enumerate(text.split('\n')):
    #             vector = vectorize(paragraph)
    #             location = {'page': page_num + 1, 'paragraph': i + 1}
    #             index.upsert(vectors=[(f"{page_num}_{i}", vector, location)])

    return index

# Search the index and get location
def search_pdf(query, index):
    vector = vectorize(query)
    print(vector)
    result = index.query(vector=[vector], top_k=1)
    print(result)
    # match_id = result['results'][0]['matches'][0]['id']
    location = result['matches'][0]['metadata']['text']
    return location

# Index the PDF document
# pdf_path = "path/to/your/document.pdf"
# index_pdf(pdf_path)

# Search and get location in PDF
# query = "Your query here"
# location = search_pdf(query)
# print("Location in PDF:", location)

import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import google.generativeai as genai
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class RAGManager:    
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        """
        Initialize RAG Manager with embedding model and load documents
        """
        try:
            self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
            self.vectorstore = None
            
            # Get directory paths from Django settings
            self.pdf_dir = "static/pdf_files/"
            self.txt_dir = "static/txt_files/"
            
            # Load and process documents
            pdf_texts = self.get_pdf_text_from_path(self.pdf_dir)
            txt_texts = self.get_txt_from_path(self.txt_dir)
            all_texts = {**pdf_texts, **txt_texts}
            
            if not all_texts:
                raise ValueError("No documents found in specified directories")
            
            # Process all texts into chunks
            all_chunks = []
            for text in all_texts.values():
                chunks = self.divide_text(text)
                all_chunks.extend(chunks)
                
            self.initialize_faiss(all_chunks)
            
        except Exception as e:
            raise ImproperlyConfigured(f"Failed to initialize RAG Manager: {str(e)}")

    def initialize_faiss(self, chunks):
        """
        Initialize FAISS database with document chunks
        """
        if not chunks:
            raise ValueError("No chunks provided for FAISS initialization")
        self.vectorstore = FAISS.from_texts(chunks, self.embedding_model)
    
    def get_pdf_text_from_path(self, directory_path):
        """
        Extract text from all PDF files in directory
        """
        pdf_texts = {}
        try:
            pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(directory_path, pdf_file)
                pdf_texts[pdf_file] = self.extract_text_from_pdf(pdf_path)
        except Exception as e:
            raise IOError(f"Error processing PDF files: {str(e)}")
        return pdf_texts

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a single PDF file
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            return text
        except Exception as e:
            raise IOError(f"Error extracting text from PDF {pdf_path}: {str(e)}")
    
    def extract_text_from_txt(self, txt_path):
        """
        Extract text from a single TXT file
        """
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Error reading TXT file {txt_path}: {str(e)}")
    
    def get_txt_from_path(self, directory):
        """
        Extract text from all TXT files in directory
        """
        txt_texts = {}
        try:
            txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
            for txt_file in txt_files:
                txt_path = os.path.join(directory, txt_file)
                txt_texts[txt_file] = self.extract_text_from_txt(txt_path)
        except Exception as e:
            raise IOError(f"Error processing TXT files: {str(e)}")
        return txt_texts

    def divide_text(self, text, max_length=1000, overlap=100):
        """
        Divide text into overlapping chunks
        """
        if not text:
            return []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_length,
            chunk_overlap=overlap
        )
        return text_splitter.split_text(text)

    def search_in_faiss(self, query, top_k=5):
        """
        Search for similar text chunks in FAISS database
        """
        if self.vectorstore is None:
            raise ValueError("FAISS database not initialized")
        if not query:
            raise ValueError("Query cannot be empty")
        return self.vectorstore.similarity_search(query, k=top_k)
    
    def send_query_to_gemini(self, final_prompt):
        """
        Send query to Gemini API
        """
        try:
            load_dotenv()
            api_key = os.getenv("GENAI_API_KEY")
            if not api_key:
                raise ValueError("GENAI_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(final_prompt)
            return response.text
            
        except Exception as e:
            raise Exception(f"Error querying Gemini API: {str(e)}")
    
    def send_query_to_rag(self, query):
        """
        Process query through RAG pipeline
        """
        try:
            if not query:
                raise ValueError("Query cannot be empty")
                
            results = self.search_in_faiss(query)
            if not results:
                return "No relevant information found in the knowledge base."
                
            context = "\n".join([result.page_content for result in results])
            final_prompt = f"Query: {query}\n\nContext:\n{context}\n\nAnswer:"
            
            return self.send_query_to_gemini(final_prompt)
            
        except Exception as e:
            raise Exception(f"Error processing RAG query: {str(e)}")
     
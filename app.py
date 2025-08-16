import streamlit as st
from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
import torch
from sentence_transformers import SentenceTransformer
import tempfile
import os
import numpy as np
import PyPDF2
import docx
import glob
import json
from typing import List, Union
from transformers import AutoTokenizer, AutoModel

# Page configuration
st.set_page_config(
    page_title="Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Base styles */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        background-color: #000000;
        border: 1px solid #333333;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
    }
    .chat-message.user {
        margin-left: 20%;
        border-color: #444444;
    }
    .chat-message.assistant {
        margin-right: 20%;
        border-color: #444444;
    }
    
    /* Input box */
    .stTextInput > div > div > input {
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #333333;
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #000000;
        border-right: 1px solid #333333;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #000000;
        color: white;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 8px 16px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mode" not in st.session_state:
    st.session_state.mode = "Chat Only"
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Mistral-7B (Balanced)"
if "llm" not in st.session_state:
    st.session_state.llm = None
if "embedder" not in st.session_state:
    st.session_state.embedder = None
if "is_initialized" not in st.session_state:
    st.session_state.is_initialized = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "embedding_model_loaded" not in st.session_state:
    st.session_state.embedding_model_loaded = False

# Custom embeddings class using InLegalBERT
class CustomEmbeddings(Embeddings):
    def __init__(self):
        try:
            # Force local-only loading for INLegalBERT
            self.tokenizer = AutoTokenizer.from_pretrained("models/InLegalBERT")
            self.model = AutoModel.from_pretrained("models/InLegalBERT")
            self.model.eval()  # Set to evaluation mode
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            st.session_state.embedding_model_loaded = True
        except Exception as e:
            st.error("Failed to load INLegalBERT from local files. Please ensure all required files (config.json, pytorch_model.bin, tokenizer_config.json, special_tokens_map.json, vocab.txt) are present in models/InLegalBERT.\nError: " + str(e))
            st.session_state.embedding_model_loaded = False
            self.model = None
            self.tokenizer = None

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded")
        
        embeddings = []
        with torch.no_grad():
            for text in texts:
                # Tokenize and prepare input
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # Get model output
                outputs = self.model(**inputs)
                # Use mean pooling of last hidden states
                last_hidden = outputs.last_hidden_state
                attention_mask = inputs['attention_mask']
                token_embeddings = last_hidden
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                embedding = sum_embeddings / sum_mask
                embeddings.append(embedding[0].cpu().numpy().tolist())
        
        return embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            return self._get_embeddings(texts)
        except Exception as e:
            st.error(f"Error in embed_documents: {str(e)}")
            return [[0.0] * 768] * len(texts)

    def embed_query(self, text: str) -> List[float]:
        try:
            return self._get_embeddings([text])[0]
        except Exception as e:
            st.error(f"Error in embed_query: {str(e)}")
            return [0.0] * 768

    def __call__(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)

# Initialize models only when needed
def initialize_models():
    if not st.session_state.is_initialized:
        with st.spinner("Initializing models (this may take a minute)... This is a one-time setup."):
            try:
                # Initialize InLegalBERT (local)
                if st.session_state.embedder is None:
                    st.session_state.embedder = CustomEmbeddings()
                # Initialize Mistral-7B (local, Q4_K_M.gguf)
                if st.session_state.llm is None:
                    st.session_state.llm = CTransformers(
                        model="models/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
                        model_type="mistral",
                        config={
                            'max_new_tokens': 512,
                            'temperature': 0.7,
                            'context_length': 2048,
                            'gpu_layers': 0
                        }
                    )
                st.session_state.is_initialized = True
                st.success("Models initialized successfully!")  # Model status only, keep
            except Exception as e:
                st.error(f"Error during model initialization: {str(e)}")
                st.info("Please check your local model files and try again.")
                return

if "legal_kb" not in st.session_state:
    st.session_state.legal_kb = None
    
if "legal_dictionary" not in st.session_state:
    st.session_state.legal_dictionary = {}

DATA_DIR = "mini_dataset"
LEGAL_CASES_PATH = os.path.join(DATA_DIR, "mini_legal_cases.txt")
LEGAL_DICT_PATH = os.path.join(DATA_DIR, "mini_legal_dictionary.txt")
QA_PATH = os.path.join(DATA_DIR, "mini_train.jsonl")

# Load legal datasets
@st.cache_data(show_spinner=False)
def load_legal_cases():
    """Load legal case files from local dataset"""
    try:
        # Define path to local case file
        case_file = LEGAL_CASES_PATH
        
        # Load case text
        try:
            with open(case_file, 'r', encoding='utf-8') as f:
                case_text = f.read()
                return case_text
        except Exception as e:
            st.warning(f"Could not load case file {case_file}: {str(e)}")
            return ""
    except Exception as e:
        st.error(f"Error loading legal case files: {str(e)}")
        return ""

@st.cache_data(show_spinner=False)
def load_legal_dictionary():
    """Load legal dictionary from local dataset"""
    try:
        dictionary_path = LEGAL_DICT_PATH
        legal_dict = {}
        
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            terms = f.readlines()
            for term in terms:
                term = term.strip()
                if term:
                    # Store terms in dictionary (we don't have definitions, just terms)
                    legal_dict[term] = True
                    
        return legal_dict
    except Exception as e:
        st.error(f"Error loading legal dictionary: {str(e)}")
        return {}

@st.cache_data(show_spinner=False)
def load_indian_legal_qa():
    """Load Indian legal Q&A data from train.jsonl file"""
    try:
        qa_file = QA_PATH
        qa_text = ""
        
        try:
            with open(qa_file, 'r', encoding='utf-8') as f:
                # The file begins with [ and likely ends with ], so we read the content and parse it as JSON
                content = f.read()
                # Parse the JSON content
                qa_data = json.loads(content)
                
                # Extract Q&A pairs and format them for our knowledge base
                for item in qa_data:
                    if "Instruction" in item and "Response" in item:
                        question = item["Instruction"]
                        answer = item["Response"]
                        # Format as "Q: ... A: ..." for the knowledge base
                        qa_text += f"Q: {question}\nA: {answer}\n\n"
                
                return qa_text
        except Exception as e:
            st.warning(f"Could not load or parse Indian legal Q&A file {qa_file}: {str(e)}")
            return ""
    except Exception as e:
        st.error(f"Error loading Indian legal Q&A data: {str(e)}")
        return ""

PERSIST_KB_DIR = "faiss_index"  # Directory to cache FAISS index

def initialize_legal_knowledge_base():
    """
    Build or load FAISS index from mini_dataset and extra_dataset (Indian law Q&A/statutes).
    Auto-build if missing. Use InLegalBERT for embeddings.
    Adds detailed debug output to help diagnose loading/building failures.
    """
    import glob
    import traceback
    # === CHECKPOINT: Using LegalKB_FAISS for IPC retrieval ===
    kb_dir = os.path.join("LegalKB_FAISS", "ipc_embed_db")
    index_faiss = os.path.join(kb_dir, "index.faiss")
    index_pkl = os.path.join(kb_dir, "index.pkl")
    if st.session_state.get("legal_kb") is not None:
        st.write("[DEBUG] legal_kb already initialized in session state.")
        return
    st.write(f"[DEBUG] Checking for FAISS index at: {index_faiss}, {index_pkl}")
    if os.path.exists(index_faiss) and os.path.exists(index_pkl):
        try:
            st.write("[DEBUG] Found FAISS index files. Attempting to load...")
            st.session_state.legal_kb = FAISS.load_local(kb_dir, st.session_state.embedder, allow_dangerous_deserialization=True)
            st.success("Loaded FAISS knowledge base from disk.")
            return
        except Exception as e:
            st.error(f"[DEBUG] Error loading FAISS index: {e}\n{traceback.format_exc()}")
    # Otherwise, build from all available Indian law data
    st.write("[DEBUG] Building FAISS knowledge base from Indian law datasets (mini_dataset + extra_dataset)...")
    all_docs = []
    # Load mini_dataset
    mini_cases = os.path.join("mini_dataset", "mini_legal_cases.txt")
    mini_dict = os.path.join("mini_dataset", "mini_legal_dictionary.txt")
    mini_qa = os.path.join("mini_dataset", "mini_train.jsonl")
    st.write(f"[DEBUG] Checking mini_dataset files: {mini_cases}, {mini_dict}, {mini_qa}")
    if os.path.exists(mini_cases):
        st.write(f"[DEBUG] Loading: {mini_cases}")
        try:
            with open(mini_cases, "r", encoding="utf-8") as f:
                all_docs.append(f.read())
        except Exception as e:
            st.error(f"[DEBUG] Failed to load {mini_cases}: {e}")
    else:
        st.warning(f"[DEBUG] File not found: {mini_cases}")
    if os.path.exists(mini_dict):
        st.write(f"[DEBUG] Loading: {mini_dict}")
        try:
            with open(mini_dict, "r", encoding="utf-8") as f:
                all_docs.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            st.error(f"[DEBUG] Failed to load {mini_dict}: {e}")
    else:
        st.warning(f"[DEBUG] File not found: {mini_dict}")
    if os.path.exists(mini_qa):
        st.write(f"[DEBUG] Loading: {mini_qa}")
        try:
            with open(mini_qa, "r", encoding="utf-8") as f:
                try:
                    qa_items = json.load(f)
                    for item in qa_items:
                        if isinstance(item, dict):
                            q = item.get("Instruction") or item.get("question")
                            a = item.get("output") or item.get("answer")
                            if q and a:
                                all_docs.append(f"Q: {q}\nA: {a}")
                except Exception as e:
                    st.error(f"[DEBUG] Failed to parse {mini_qa} as JSON: {e}")
        except Exception as e:
            st.error(f"[DEBUG] Failed to load {mini_qa}: {e}")
    else:
        st.warning(f"[DEBUG] File not found: {mini_qa}")
    # Load extra_dataset Q&A
    extra_files = ["ipc_qa.json", "crpc_qa.json", "constitution_qa.json", "IndicLegalQA Dataset_10K_Revised.json"]
    for fname in extra_files:
        fpath = os.path.join("extra_dataset", fname)
        st.write(f"[DEBUG] Checking extra_dataset file: {fpath}")
        if os.path.exists(fpath):
            st.write(f"[DEBUG] Loading: {fpath}")
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    try:
                        items = json.load(f)
                        for item in items:
                            q = item.get("question")
                            a = item.get("answer")
                            if q and a:
                                all_docs.append(f"Q: {q}\nA: {a}")
                    except Exception as e:
                        st.error(f"[DEBUG] Failed to parse {fpath} as JSON: {e}")
            except Exception as e:
                st.error(f"[DEBUG] Failed to load {fpath}: {e}")
        else:
            pass
    if not all_docs:
        st.session_state.legal_kb = None
        return
    # --- SPEED-UP FOR TESTING ---
    DOC_LIMIT = 300  # Change this value for more/less docs during testing
    if len(all_docs) > DOC_LIMIT:
        all_docs = all_docs[:DOC_LIMIT]
    try:
        progress_bar = st.progress(0)
        embeddings = []
        batch_size = 10
        for i in range(0, len(all_docs), batch_size):
            batch = all_docs[i:i+batch_size]
            batch_emb = st.session_state.embedder.embed_documents(batch)
            embeddings.extend(batch_emb)
            progress_bar.progress(min((i+batch_size)/len(all_docs), 1.0))
        text_embeddings = list(zip(all_docs, embeddings))
        st.session_state.legal_kb = FAISS.from_embeddings(text_embeddings, st.session_state.embedder)
        if not os.path.exists(kb_dir):
            os.makedirs(kb_dir)
        st.session_state.legal_kb.save_local(kb_dir)
        progress_bar.progress(1.0)
        st.success("Built and saved FAISS knowledge base (TEST MODE, limited docs).")
    except Exception as e:
        st.error(f"Failed to build or save FAISS knowledge base: {e}\n{traceback.format_exc()}")
        st.session_state.legal_kb = None
    finally:
        progress_bar.empty()

def read_pdf(file):
    """Read PDF file and extract text"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def process_document(uploaded_file):
    # Create a temporary file
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
    
    # Save uploaded file to the temporary file
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process based on file type
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext == ".pdf":
        with open(temp_file_path, "rb") as f:
            document_text = read_pdf(f)
    elif file_ext in [".docx", ".doc"]:
        document_text = read_docx(temp_file_path)
    else:
        document_text = "Unsupported file format"
        
    # Clean up
    temp_dir.cleanup()
    
    return document_text

def create_vector_store(document_text):
    # Split text into much smaller chunks to avoid token limits
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Increased chunk size to speed up embedding
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(document_text)
    
    # Create vectorstore
    if not chunks:
        return None
        
    try:
        # If legal knowledge base exists, merge with it
        if st.session_state.legal_kb is not None:
            # Create document vectorstore
            doc_vectorstore = FAISS.from_texts(
                texts=chunks,
                embedding=st.session_state.embedder
            )
            
            # Merge with legal KB (document content takes precedence)
            merged_vectorstore = st.session_state.legal_kb.merge_from(doc_vectorstore)
            return merged_vectorstore
        else:
            # Just use document vectorstore
            vectorstore = FAISS.from_texts(
                texts=chunks,
                embedding=st.session_state.embedder
            )
            return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None

def get_conversation_chain(vectorstore=None):
    # Initialize the LLM with more conservative settings 
    # to ensure stability in document-based discussions
    llm = st.session_state.llm
    
    # Initialize memory using the updated approach
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # This is required for the ConversationalRetrievalChain
        return_messages=True,
        output_key="answer",
        input_key="question"
    )
    
    # Initialize InLegalBERT for both chat and document modes
    if st.session_state.embedder is None:
        try:
            st.session_state.embedder = CustomEmbeddings()
        except Exception as e:
            st.error(f"Error initializing embeddings: {str(e)}")
    
    # If no specific vectorstore is provided but we have a legal KB, use that
    if vectorstore is None and st.session_state.legal_kb is not None:
        vectorstore = st.session_state.legal_kb
    
    if vectorstore:
        # Document analysis mode
        prompt_template = """
        You are a legal assistant specializing in document analysis with expertise in global and Indian legal systems. 
        Use the following pieces of context to answer the user's question.
        If the question relates to Indian law, provide specific information about Indian legal procedures, statutes, and precedents.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Chat History: {chat_history}
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),  # Reduced k for more focused answers
            memory=memory,
            combine_docs_chain_kwargs={"document_variable_name": "context"},
            return_source_documents=True,
            chain_type="stuff"
        )
    else:
        # Initialize memory for chat-only mode
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        # Chat-only mode with conversation memory
        # We'll manage memory manually for the dict-based chain
        prompt = PromptTemplate(
            input_variables=["chat_history", "question"],
            template="""
            You are a knowledgeable legal assistant with expertise in all areas of law, including Indian law.
            Answer the following question using your legal knowledge to provide a contextually relevant response.
            
            If the question relates to Indian law, provide specific information about Indian legal procedures, statutes, and precedents.
            
            Previous conversation:
            {chat_history}
            
            Question: {question}
            
            Answer:
            """
        )
        
        chain = {
            "question": lambda x: x,
            "answer": lambda x: llm.invoke(prompt.format(
                chat_history=format_chat_history(st.session_state.chat_history),
                question=x
            ))
        }
    
    return chain

# Format chat history for the prompt
def format_chat_history(chat_history):
    if not chat_history:
        return "No previous conversation."
    
    # Only use the last 3 exchanges (6 messages) to limit context size
    limited_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
    
    formatted_history = ""
    for entry in limited_history:
        # Truncate very long messages
        content = entry["content"]
        if len(content) > 200:  # Limit individual messages to 200 chars
            content = content[:197] + "..."
            
        if entry["role"] == "user":
            formatted_history += f"Human: {content}\n"
        else:
            formatted_history += f"Assistant: {content}\n"
    
    return formatted_history

# Get formatted chat history for LangChain
def get_langchain_history(chat_history):
    if not chat_history:
        return []
        
    # Only use the last 3 exchanges to limit context size
    # Each exchange is a (user, assistant) pair
    formatted_history = []
    
    # Process in reverse to get most recent exchanges first
    i = len(chat_history) - 1
    exchanges = 0
    max_exchanges = 3
    
    while i > 0 and exchanges < max_exchanges:
        if i >= 1 and chat_history[i]["role"] == "assistant" and chat_history[i-1]["role"] == "user":
            # Truncate very long messages
            user_msg = chat_history[i-1]["content"]
            if len(user_msg) > 200:  # Limit to 200 chars
                user_msg = user_msg[:197] + "..."
                
            ai_msg = chat_history[i]["content"]
            if len(ai_msg) > 200:  # Limit to 200 chars
                ai_msg = ai_msg[:197] + "..."
                
            # Add to history in the correct order (oldest first)
            formatted_history.insert(0, (user_msg, ai_msg))
            exchanges += 1
            i -= 2
        else:
            i -= 1
            
    return formatted_history

# Strict Indian law QA prompt (single template, enforced everywhere)
QA_PROMPT = """
<s>[INST]
You are an expert assistant specializing in Indian law. Provide highly accurate, contextually appropriate, and well-structured answers strictly based on Indian legal statutes, regulations, and precedents. If you do not know the answer, say \"I don't know.\" Do not hallucinate or make up information.

CONTEXT: {legal_context}
CHAT HISTORY: {chat_history}
QUESTION: {user_question}

ANSWER:
- Detail the first key aspect of the law, ensuring it reflects general application.
- Provide a concise explanation of how the law is typically interpreted or applied.
- Correct a common misconception or clarify a frequently misunderstood aspect.
- Detail any exceptions to the general rule, if applicable.
- Include any additional relevant information that directly relates to the user's query.
</s>[INST]
"""

def is_legal_passage(text):
    # Check if text is long enough to be a passage
    if len(text) > 150:
        return True
    
    # Check if text has legal keywords
    legal_keywords = ["section", "clause", "contract", "agreement", "party", "plaintiff", 
                     "defendant", "court", "law", "statute", "regulation", "rights", 
                     "obligations", "liability", "pursuant", "herein", "thereof", 
                     "hereinafter", "aforementioned", "shall", "hereby"]
    
    for keyword in legal_keywords:
        if keyword.lower() in text.lower():
            return True
            
    return False

# Function to determine if input is asking for a definition
def is_definition_request(text):
    definition_patterns = [
        "what is",
        "define",
        "explain",
        "meaning of",
        "definition of",
        "what does",
        "what are"
    ]
    
    text_lower = text.lower()
    for pattern in definition_patterns:
        if pattern in text_lower and len(text) < 100:
            return True
            
    return False

# Function to check if a term is in our legal dictionary
def is_legal_term(text):
    """Check if text contains terms from our legal dictionary"""
    if not st.session_state.legal_dictionary:
        return False
        
    words = text.lower().split()
    for word in words:
        if word in st.session_state.legal_dictionary:
            return True
            
    # Also check for phrases (up to 4 words)
    if len(words) >= 2:
        for i in range(len(words)-1):
            phrase = words[i] + " " + words[i+1]
            if phrase in st.session_state.legal_dictionary:
                return True
                
    if len(words) >= 3:
        for i in range(len(words)-2):
            phrase = words[i] + " " + words[i+1] + " " + words[i+2]
            if phrase in st.session_state.legal_dictionary:
                return True
                
    if len(words) >= 4:
        for i in range(len(words)-3):
            phrase = words[i] + " " + words[i+1] + " " + words[i+2] + " " + words[i+3]
            if phrase in st.session_state.legal_dictionary:
                return True
                
    return False

# Function to determine if input is likely about Indian law
def is_indian_law_query(text):
    """Check if text is likely about Indian law"""
    indian_law_keywords = [
        "india", "indian", "ipc", "crpc", "constitution of india", "supreme court of india",
        "high court", "section", "article", "delhi", "mumbai", "calcutta", "madras", "pil",
        "writ", "petition", "plaint", "fir", "fundamental rights", "directive principles"
    ]
    
    text_lower = text.lower()
    for keyword in indian_law_keywords:
        if keyword in text_lower:
            return True
    
    return False

# Generate response function with improved prompt templates, legal dictionary lookup, and Indian law detection
def generate_response(prompt):
    if not st.session_state.llm_loaded:
        return "Error: Language model not loaded. Please refresh the page."
    
    # Check if input contains legal terms from our dictionary
    is_legal = is_legal_term(prompt)
    
    # Check if this is likely about Indian law
    is_indian = is_indian_law_query(prompt)
    
    # Determine the type of query
    if is_definition_request(prompt):
        template = TEMPLATES["definition"]
        final_prompt = template.format(user_question=prompt[:100])  # Limit term length
    elif is_indian and not is_legal_passage(prompt):
        # For Indian law queries that aren't passages, use the Indian law template
        template = TEMPLATES["indian_law"]
        final_prompt = template.format(user_question=prompt[:200])
    elif is_legal_passage(prompt) or is_legal:
        # For legal passages, use the reasoning template
        template = TEMPLATES["reasoning"]
        
        # If text is very long, keep only the first chunk to avoid token limits
        if len(prompt) > 800:
            legal_context = prompt[:800]
        else:
            legal_context = prompt
            
        final_prompt = template.format(
            legal_context=legal_context, 
            user_question="Explain what this means in simple terms."
        )
    else:
        # For general questions without context, use fallback
        template = TEMPLATES["fallback"]
        # Limit question length
        final_prompt = template.format(user_question=prompt[:200])

    # Generate response
    try:
        # Use a more reliable approach with error handling
        response = ""
        retry_count = 0
        max_retries = 3
        
        while not response and retry_count < max_retries:
            try:
                response = st.session_state.llm.invoke(final_prompt)
                # Check if response seems complete (ends with period, question mark, etc.)
                if response and not response.endswith((".", "!", "?", ":", ";")):
                    response = response + "..."
            except Exception as inner_e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise inner_e
                # Reduce prompt size on retry
                if len(final_prompt) > 300:
                    final_prompt = final_prompt[:300]
        
        return response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, I encountered an error. Please try again with a simpler question."

# Main UI
st.title("🦅 LegalEagle")

# Initialize models and KB
initialize_models()
initialize_legal_knowledge_base()

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    - **Embeddings**: InLegalBERT (local)
    - **LLM**: Mistral-7B (local, via ctransformers)
    - **Retrieval**: FAISS (local, Indian law Q&A/statutes)
    - **Private**: No cloud APIs required
    """)
    st.markdown("---")
    st.markdown("**Disclaimer:** This tool provides general information only, not legal advice. Always consult a qualified legal professional for advice on specific situations.")
    st.markdown("---")
    st.markdown("**Example Questions:**\n- What is Article 21 of the Indian Constitution?\n- How do I file a complaint against my employer in India?\n- What is Section 420 IPC?\n\nWelcome to LegalEagle!")

# Chat interface
st.markdown("""---\n#### Chat with LegalEagle\n---""")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat():
    st.session_state.messages = []
    st.session_state.chat_history = []

# Add a clear chat button below the chat interface
if st.button('🗑️ Clear Chat', key='clear_chat_button'):
    clear_chat()
    st.success('Chat cleared! Please enter a new question to start over.')
    st.stop()

input_prompt = st.chat_input("Ask your Indian law question...")
# --- Chat message handling: strictly enforce Indian law prompt ---
if input_prompt:
    with st.chat_message("user"):
        st.markdown(f"**You:** {input_prompt}")
    st.session_state.messages.append({"role": "user", "content": input_prompt})

    kb = st.session_state.legal_kb
    if kb is None:
        st.error("Legal knowledge base is not loaded. Please restart the app or check your dataset files.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking 💡..."):
                retriever = kb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                docs = retriever.get_relevant_documents(input_prompt)
                context = "\n\n".join([d.page_content for d in docs])
                # Enforce strict Indian law QA prompt
                prompt = QA_PROMPT.format(legal_context=context, user_question=input_prompt, chat_history=format_chat_history(st.session_state.chat_history))
                answer = st.session_state.llm(prompt)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
# All legacy and unreachable code below this point removed for clarity and to resolve indentation errors.

# Sidebar for information and examples
with st.sidebar:
    st.header("Legal Assistant Features")
    st.markdown("""
    This assistant can:
    
    - **Explain legal terms** in plain English
    - **Analyze legal passages** from contracts, agreements, etc.
    - **Answer legal questions** with proper reasoning
    - **Use a knowledge base** of legal cases and terminology
    - **Provide Indian legal expertise** on statutes, procedures, and cases
    """)
    
    st.header("Example Questions")
    st.markdown("""
    **Legal Terms:**
    - What is habeas corpus?
    - Define prima facie
    - What is tortious interference?
    
    **Legal Analysis:**
    - *Paste a clause from a contract*
    - *Paste a legal provision*
    
    **Case Law:**
    - What did the Supreme Court rule about partnerships in taxation?
    - Explain the A. W. Figgies case
    
    **Indian Law Questions:**
    - What is the difference between a petition and a plaint in Indian law?
    - What is the procedure for filing an FIR in India?
    - Explain Article 21 of the Indian Constitution
    """)
    
    st.header("Usage Tips")
    st.markdown("""
    - For legal terms, start with "what is" or "define"
    - For legal passages, just paste the text
    - For best results, keep questions clear and specific
    - For Indian law questions, mention "India" or specific Indian legal terms
    """)
    
    # Add model information
    st.header("Models")
    st.markdown(f"""
    - **Current Model**: {st.session_state.selected_model}
    - **Embeddings**: all-MiniLM-L6-v2
    - **Knowledge Base**: Legal terminology, case law, and Indian legal Q&A data
    
    **Model Info**:
    - **Mistral-7B**: Higher quality, more nuanced responses (better for complex legal questions)
    - **Phi-2**: Faster responses, smaller context window (better for simple queries)
    """)
    
    # Add a disclaimer
    st.markdown("---")
    st.markdown("""
    **Disclaimer**: This tool provides general information only, not legal advice. 
    Always consult a qualified legal professional for advice on specific situations.
    """)
    
    # KB status
    if st.session_state.get("legal_kb") is not None:
        st.info("FAISS legal knowledge base loaded from LegalKB_FAISS/ipc_embed_db.")
    else:
        st.warning("FAISS knowledge base not loaded.")
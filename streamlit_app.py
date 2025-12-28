# streamlit_app.py

import os
import tempfile
import streamlit as st
import pandas as pd
import io

from pathlib import Path
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_groq import ChatGroq
from llama_parse import LlamaParse

# Import the new utility functions
from utils import getStockTickers, getCandlestickChartData

# --- Page Configuration ---
st.set_page_config(
    page_title="Your AI Financial Analyser",
    page_icon="🤖",
    layout="wide"
)

# --- API KEY and Environment Setup ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_PARSE_KEY = os.getenv("LLAMA_PARSE_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# --- Caching and RAG Chain Building ---
@st.cache_resource(show_spinner="Reading your document...")
def build_rag_chain(_uploaded_file):
    """Builds the RAG chain from an uploaded file and returns it."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(_uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    parser = LlamaParse(api_key=LLAMA_PARSE_KEY, result_type="markdown")
    documents = parser.load_data(tmp_file_path)
    os.remove(tmp_file_path)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([documents[0].text])

    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    qdrant = Qdrant.from_documents(docs, embeddings, location=":memory:", collection_name=f"doc_{_uploaded_file.file_id}")

    retriever = qdrant.as_retriever(search_kwargs={"k": 10})
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

    # A more conversational prompt template
    prompt_template = """
    You are a helpful and friendly financial assistant. Your goal is to help the user understand their document.
    Use the following pieces of context to answer the user's question clearly and concisely.
    If you don't know the answer, just say that you're not sure but you'll do your best to help.
    When asked to provide data from a table, please format it as a clean, simple markdown table.

    Context: {context}
    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=compression_retriever,
        return_source_documents=True, chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "active_document" not in st.session_state:
    st.session_state.active_document = None
if "last_active_doc" not in st.session_state:
    st.session_state.last_active_doc = None


# --- UI Rendering ---
st.title("Welcome to your AI Financial Analyser! 🤖")

# --- Sidebar for Global Controls ---
with st.sidebar:
    st.header("What would you like to do?")

    # Document Management Section
    st.subheader("Chat with a Document")
    if st.button("Load Example Financial Report (NVIDIA)"):
        with st.spinner("Loading example..."):
            file_name = "NVIDIAAn.pdf"
            if os.path.exists(file_name):
                 with open(file_name, "rb") as f:
                    bytes_data = f.read()
                 st.session_state.uploaded_files[file_name] = {"data": bytes_data, "file_id": file_name}
                 st.session_state.active_document = file_name
            else:
                 st.error("Example file 'NVIDIAAn.pdf' not found. Please add it to your project folder.")

    uploaded_files_list = st.file_uploader("Upload some PDFs to get started!", type="pdf", accept_multiple_files=True)
    if uploaded_files_list:
        for uploaded_file in uploaded_files_list:
            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files[uploaded_file.name] = {"data": uploaded_file.getvalue(), "file_id": uploaded_file.file_id}
        if not st.session_state.active_document:
            st.session_state.active_document = list(st.session_state.uploaded_files.keys())[0]

    if st.session_state.uploaded_files:
        st.session_state.active_document = st.selectbox(
            "Which document should we chat about?",
            options=list(st.session_state.uploaded_files.keys()),
            key="doc_selector"
        )
    st.markdown("---")

    # Stock Selector Section
    st.subheader("Check Live Stocks")
    stockTickers = getStockTickers()
    selectedTicker = st.selectbox("Pick a stock to see its performance", stockTickers)

# --- Main Interface with Tabs ---
tab1, tab2 = st.tabs(["Chat with a Doc 📄", "Live Stock Charts 📈"])

# --- RAG Chat Tab ---
with tab1:
    if st.session_state.active_document:
        st.header(f"Let's chat about: *{st.session_state.active_document}*")
        
        # Add a welcome message from the assistant if the document has just been loaded/selected
        if st.session_state.active_document != st.session_state.get('last_active_doc'):
            st.session_state.last_active_doc = st.session_state.active_document
            st.session_state.messages = [{"role": "assistant", "content": f"I've finished reading **{st.session_state.active_document}**! What financial insights can I help you with?"}]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "chart_data" in message:
                    st.bar_chart(message["chart_data"])

        if prompt := st.chat_input(f"Ask me anything about {st.session_state.active_document}..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Finding the answer..."):
                    try:
                        active_doc_data = st.session_state.uploaded_files[st.session_state.active_document]
                        bytes_io = io.BytesIO(active_doc_data["data"])
                        bytes_io.name = st.session_state.active_document
                        bytes_io.file_id = active_doc_data["file_id"]

                        qa_chain = build_rag_chain(bytes_io)
                        response = qa_chain.invoke(prompt)
                        response_text = response["result"]
                        st.markdown(response_text)

                        try:
                            tables = pd.read_html(io.StringIO(response_text))
                            if tables:
                                df = tables[0].dropna(how='all').astype(str)
                                if len(df.columns) > 1 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                                    df = df.set_index(df.columns[0])
                                    st.bar_chart(df)
                                    assistant_message = {"role": "assistant", "content": response_text, "chart_data": df}
                                else:
                                    assistant_message = {"role": "assistant", "content": response_text}
                            else:
                                 assistant_message = {"role": "assistant", "content": response_text}
                        except Exception:
                            assistant_message = {"role": "assistant", "content": response_text}

                        with st.expander("Show Sources"):
                            for i, source_doc in enumerate(response["source_documents"]):
                                st.markdown(f"*Source {i+1}*")
                                st.markdown(source_doc.page_content.replace("$", "\\$"))
                        st.session_state.messages.append(assistant_message)
                    except Exception as e:
                        error_message = f"Oh no, an error occurred: {e}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        st.info("Hello! I'm ready to help you analyze financial documents. To get started, please upload a PDF or load the example report using the sidebar on the left. 😊")

# --- Stock Analysis Tab ---
with tab2:
    st.header(f"Here's the latest for {selectedTicker} 📈")
    historicalData, candlestickChart = getCandlestickChartData(selectedTicker)

    if not historicalData.empty:
        st.subheader("Price Action (Last Year)")
        st.plotly_chart(candlestickChart, use_container_width=True)

        st.subheader("Historical Price Data")
        st.dataframe(historicalData, height=350, use_container_width=True)
    else:
        st.error(f"Hmm, I couldn't retrieve the data for {selectedTicker}. Please try another ticker.")
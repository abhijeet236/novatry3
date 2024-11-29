import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from groq import Groq

def read_pdf(file):
    """Read text from a PDF file."""
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def process_pdfs(files):
    """Process uploaded PDF files to create embeddings and FAISS index."""
    progress_bar = st.sidebar.progress(0)
    st.sidebar.write("🔄 Processing the PDFs...")

    try:
        documents = []
        for i, file in enumerate(files):
            content = read_pdf(file)
            if content:
                documents.append(content)
            progress_bar.progress((i + 1) / len(files) * 0.5)

        if not documents:
            raise ValueError("No valid content could be fetched from the provided PDFs.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        split_docs = splitter.create_documents(documents)
        progress_bar.progress(0.7)

        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        st.session_state.faiss_index = FAISS.from_documents(split_docs, embedding_model)

        progress_bar.progress(1.0)
        st.sidebar.success("✅ Processing completed!")
        st.session_state.pdfs_processed = True
    except Exception as e:
        st.sidebar.error(f"An error occurred during analysis: {str(e)}")
        st.session_state.pdfs_processed = False
    finally:
        progress_bar.empty()

def chat_interface():
    """Main chat interface with question answering."""
    st.header("📝 Ask Your Questions")

    # Initialize chat history if it does not exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User interface for query
    query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if not st.session_state.pdfs_processed:
            st.error("Please analyze the PDFs first.")
        elif not query:
            st.warning("Please enter a question before submitting.")
        else:
            try:
                with st.spinner("Generating the answer..."):
                    results = st.session_state.faiss_index.similarity_search(query, k=6)

                    if results:
                        context = "\n".join([doc.page_content for doc in results])

                        # Initialize the Groq client
                        groq_api_key = "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"
                        client = Groq(api_key=groq_api_key)

                        chat_context = "\n".join(
                            [f"User: {msg['question']}\nNOVA: {msg['answer']}" for msg in st.session_state.chat_history]
                        )
                        chat_input = f"{chat_context}\nUser: {query}"

                        completion = client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=[
                                {"role": "system", "content": "You are NOVA, an organizational assistant."},
                                {"role": "user", "content": f"Context: {context}\n\nChat history: {chat_input}\n\nPlease answer the question based on the given context."}
                            ],
                            temperature=0.5,
                            max_tokens=1024
                        )

                        answer = completion.choices[0].message.content
                        st.markdown(f"**Question:** {query}")
                        st.markdown(
                            f"<div style='background-color: #262730; padding: 10px; border-radius: 5px;'><strong>NOVA:</strong> {answer}</div>",
                            unsafe_allow_html=True
                        )

                        st.session_state.chat_history.append({"question": query, "answer": answer})
                    else:
                        st.error("No relevant information found to answer the question.")
            except Exception as e:
                st.error(f"An error occurred while generating the answer: {str(e)}")

    # Display chat history
    st.header("🕒 Chat History")
    for msg in st.session_state.chat_history:
        st.markdown(f"**User:** {msg['question']}")
        st.markdown(
            f"<div style='background-color: #262730; padding: 10px; border-radius: 5px;'><strong>NOVA:</strong> {msg['answer']}</div>",
            unsafe_allow_html=True
        )

    # Admin functionality for uploading PDFs
    if 'role' in st.session_state and st.session_state.role == "admin":
        st.sidebar.subheader("Upload PDFs for Analysis")
        uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
        if st.sidebar.button("Analyze PDFs"):
            if uploaded_files:
                process_pdfs(uploaded_files)
            else:
                st.sidebar.warning("Please upload at least one PDF file.")

chat_interface()

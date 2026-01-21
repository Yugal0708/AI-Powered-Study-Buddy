import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="AI-Powered Study Buddy",
    page_icon="📚",
    layout="wide"
)

# Configure Gemini API (you'll need to get a free API key from https://ai.google.dev)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .student-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with student info
st.markdown("""
    <div class="student-info">
        <h2>🎓 AI-Powered Study Buddy</h2>
        <p><strong>Developed by:</strong> Yugal Dhanraj Bilawane</p>
        <p><strong>College:</strong> Dharampeth M.P Deo Memorial Science College, Nagpur</p>
        <p><strong>Department:</strong> Data Science</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📚 Study Tools")
feature = st.sidebar.radio(
    "Choose a feature:",
    ["🏠 Home", "💡 Concept Explainer", "📝 Summarizer", "❓ Quiz Generator", "🗂️ Flashcard Creator", "💬 Ask Questions"]
)

# Function to read PDF
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to read DOCX
def read_docx(file):
    doc = Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to get AI response
def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease make sure you've added your Gemini API key!"

# HOME PAGE
if feature == "🏠 Home":
    st.title("Welcome to Your AI Study Buddy! 👋")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What Can I Do?
        
        Your personal AI-powered learning assistant that helps you:
        - **Understand complex concepts** in simple terms
        - **Summarize long study materials** quickly
        - **Generate practice quizzes** for any topic
        - **Create flashcards** for efficient revision
        - **Answer your questions** 24/7
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 How to Use?
        
        1. Select a feature from the sidebar
        2. Enter your topic or upload study material
        3. Get instant AI-powered assistance
        4. Save and review generated content
        
        **Tip:** You can upload PDF, TXT, or DOCX files!
        """)
    
    st.info("👈 Select a feature from the sidebar to get started!")

# CONCEPT EXPLAINER
elif feature == "💡 Concept Explainer":
    st.title("💡 Concept Explainer")
    st.write("Get simple explanations for complex topics!")
    
    topic = st.text_input("Enter the concept you want to understand:")
    difficulty = st.select_slider(
        "Select difficulty level:",
        options=["Beginner", "Intermediate", "Advanced"]
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        subject = st.selectbox(
            "Subject area:",
            ["General", "Mathematics", "Science", "Computer Science", "History", "Literature", "Other"]
        )
    
    if st.button("Explain", type="primary"):
        if topic:
            with st.spinner("Generating explanation..."):
                prompt = f"""
                Explain the concept of "{topic}" in {difficulty} level terms for a {subject} student.
                Make it clear, concise, and include:
                1. Simple definition
                2. Key points to remember
                3. Real-world example or analogy
                4. Common misconceptions (if any)
                
                Keep the explanation engaging and easy to understand.
                """
                explanation = get_ai_response(prompt)
                st.success("✅ Explanation Generated!")
                st.markdown(explanation)
                
                # Download option
                st.download_button(
                    "📥 Download Explanation",
                    explanation,
                    file_name=f"{topic}_explanation.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a concept to explain!")

# SUMMARIZER
elif feature == "📝 Summarizer":
    st.title("📝 Smart Summarizer")
    st.write("Condense long study materials into key points!")
    
    input_method = st.radio("Choose input method:", ["📝 Text Input", "📁 File Upload"])
    
    text_content = ""
    
    if input_method == "📝 Text Input":
        text_content = st.text_area("Paste your study material here:", height=200)
    else:
        uploaded_file = st.file_uploader("Upload your file", type=["pdf", "txt", "docx"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                text_content = read_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                text_content = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text_content = read_docx(uploaded_file)
            
            st.success(f"✅ File uploaded! ({len(text_content)} characters)")
    
    summary_length = st.select_slider(
        "Summary length:",
        options=["Brief", "Moderate", "Detailed"]
    )
    
    if st.button("Generate Summary", type="primary"):
        if text_content:
            with st.spinner("Creating summary..."):
                prompt = f"""
                Summarize the following text in {summary_length} format.
                
                Create a {summary_length.lower()} summary with:
                - Main points and key concepts
                - Important facts and figures
                - Clear structure with bullet points
                
                Text to summarize:
                {text_content[:10000]}  # Limit to prevent token overflow
                """
                summary = get_ai_response(prompt)
                st.success("✅ Summary Generated!")
                st.markdown(summary)
                
                st.download_button(
                    "📥 Download Summary",
                    summary,
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please provide text to summarize!")

# QUIZ GENERATOR
elif feature == "❓ Quiz Generator":
    st.title("❓ Quiz Generator")
    st.write("Generate practice questions from any topic!")
    
    topic = st.text_input("Enter the topic for quiz:")
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of questions:", 3, 15, 5)
    with col2:
        question_type = st.selectbox(
            "Question type:",
            ["Multiple Choice", "True/False", "Short Answer", "Mixed"]
        )
    
    difficulty = st.select_slider(
        "Difficulty level:",
        options=["Easy", "Medium", "Hard"]
    )
    
    if st.button("Generate Quiz", type="primary"):
        if topic:
            with st.spinner("Creating quiz questions..."):
                prompt = f"""
                Generate {num_questions} {question_type} questions about "{topic}" at {difficulty} difficulty level.
                
                Format each question as:
                Q[number]. [Question]
                A) [Option 1]
                B) [Option 2]
                C) [Option 3]
                D) [Option 4]
                Correct Answer: [Letter]
                Explanation: [Brief explanation]
                
                Make questions challenging yet fair. Include practical applications where possible.
                """
                quiz = get_ai_response(prompt)
                st.success("✅ Quiz Generated!")
                st.markdown(quiz)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download Quiz",
                        quiz,
                        file_name=f"{topic}_quiz.txt",
                        mime="text/plain"
                    )
        else:
            st.warning("Please enter a topic for the quiz!")

# FLASHCARD CREATOR
elif feature == "🗂️ Flashcard Creator":
    st.title("🗂️ Flashcard Creator")
    st.write("Create digital flashcards for quick revision!")
    
    topic = st.text_input("Enter the topic for flashcards:")
    num_cards = st.slider("Number of flashcards:", 5, 20, 10)
    
    if st.button("Create Flashcards", type="primary"):
        if topic:
            with st.spinner("Creating flashcards..."):
                prompt = f"""
                Create {num_cards} flashcards about "{topic}".
                
                Format each flashcard as:
                
                CARD [number]:
                FRONT: [Question or term]
                BACK: [Answer or definition with brief explanation]
                ---
                
                Make flashcards concise and focused on key concepts.
                Include important terms, formulas, dates, or definitions.
                """
                flashcards = get_ai_response(prompt)
                st.success("✅ Flashcards Created!")
                
                # Display flashcards in a nice format
                cards = flashcards.split("---")
                for i, card in enumerate(cards):
                    if card.strip():
                        with st.expander(f"📇 Flashcard {i+1}", expanded=(i==0)):
                            st.markdown(card)
                
                st.download_button(
                    "📥 Download All Flashcards",
                    flashcards,
                    file_name=f"{topic}_flashcards.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a topic for flashcards!")

# ASK QUESTIONS
elif feature == "💬 Ask Questions":
    st.title("💬 Ask Me Anything!")
    st.write("Your 24/7 study companion for instant doubt resolution!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])
    
    # Chat input
    user_question = st.chat_input("Ask your question here...")
    
    if user_question:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                prompt = f"""
                As an AI Study Buddy, answer this student's question clearly and helpfully:
                
                Question: {user_question}
                
                Provide:
                1. A clear, direct answer
                2. Additional context or explanation if needed
                3. Related concepts they might want to explore
                4. Encouragement and study tips if appropriate
                
                Be friendly, supportive, and educational.
                """
                response = get_ai_response(prompt)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Developed by Yugal Dhanraj Bilawane | Dharampeth M.P Deo Memorial Science College, Nagpur</p>
        <p>Powered by Google Gemini AI | © 2026</p>
    </div>
""", unsafe_allow_html=True)

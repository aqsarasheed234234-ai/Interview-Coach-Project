import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import PyPDF2
import io

# 1. Load API Key from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# 2. Stop the app if API Key is missing
if not groq_api_key:
    st.error("⚠️ Please add your Groq API Key as 'GROQ_API_KEY' in the .env file.")
    st.stop()

# 3. Initialize Groq's Llama model
@st.cache_resource
def load_llm():
    return ChatGroq(
        temperature=0.7,
        groq_api_key=groq_api_key,
        model_name="llama3-70b-8192"  # Free and fastest model
    )

llm = load_llm()

# 4. Streamlit UI Configuration
st.set_page_config(page_title="AI Interview Coach", page_icon="🎯")
st.title("🎯 AI Interview Coach")
st.markdown("Tell us your skills and practice interviews with AI.")

# --- Sidebar: User Profile ---
with st.sidebar:
    st.header("👤 Your Profile")
    name = st.text_input("Your Name")
    role = st.text_input("Job Title (e.g., Data Scientist, MERN Developer)")
    tech_stack = st.text_area("Your Skills (Tech Stack) - separate with commas", placeholder="e.g., Python, Machine Learning, React, Node.js")
    
    uploaded_file = st.file_uploader("Or upload your CV (PDF)", type="pdf")
    
    start_interview = st.button("🚀 Start Interview")

# --- Main Area: Interview Process ---
if 'questions' not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.interview_active = False
    st.session_state.interview_complete = False

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        st.error(f"Error reading CV: {e}")
        return ""

# When user clicks "Start Interview"
if start_interview:
    if not tech_stack and not uploaded_file:
        st.warning("⚠️ Please type your skills or upload a CV.")
        st.stop()
    
    with st.spinner("🤖 AI is preparing questions..."):
        # If CV is uploaded, extract text
        if uploaded_file:
            cv_text = extract_text_from_pdf(uploaded_file)
            if cv_text:
                tech_stack = cv_text  # Use entire CV as tech_stack
            else:
                st.warning("CV is empty or couldn't be read. Please type your skills manually.")
                st.stop()
        
        # --- Build the prompt (NEW LangChain 0.3 syntax) ---
        prompt_template = ChatPromptTemplate.from_template("""
        You are a professional interviewer.
        Based on the following role and skills, generate exactly 5 unique and challenging technical questions.
        List the questions from number 1 to 5 in order.
        
        Role: {role}
        Skills/Experience: {skills}
        
        Questions:
        """)
        
        # Using the new pipeline syntax (|) instead of LLMChain
        chain = prompt_template | llm | StrOutputParser()
        
        # If user didn't enter a role, use default
        if not role:
            role = "Software Developer"
        
        # Generate questions using invoke() instead of run()
        response = chain.invoke({"role": role, "skills": tech_stack})
        
        # Parse questions (extract numbered questions)
        questions_list = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-')):
                # Remove numbers or bullet points
                if line[0].isdigit():
                    # Convert "1. Question" to "Question"
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        questions_list.append(parts[1].strip())
                    else:
                        questions_list.append(line)
                else:
                    questions_list.append(line.lstrip('•- '))
        
        # If no questions found, use the entire response as one question
        if not questions_list:
            questions_list = [response]
        
        # Keep only 5 questions
        questions_list = questions_list[:5]
        
        # Save to session state
        st.session_state.questions = questions_list
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.session_state.feedback = []
        st.session_state.interview_active = True
        st.session_state.interview_complete = False
        
        st.success(f"✅ {len(questions_list)} questions have been prepared!")

# --- Interview Process ---
if st.session_state.interview_active and not st.session_state.interview_complete:
    current_q = st.session_state.current_q
    questions = st.session_state.questions
    
    if current_q < len(questions):
        st.subheader(f"Question {current_q + 1} of {len(questions)}")
        st.write(f"**{questions[current_q]}**")
        
        # Text area for user's answer
        user_answer = st.text_area("Type your answer here:", key=f"answer_{current_q}", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Submit Answer", key=f"submit_{current_q}"):
                if user_answer.strip():
                    # --- Generate Feedback (NEW LangChain 0.3 syntax) ---
                    with st.spinner("🤖 Analyzing your answer..."):
                        feedback_prompt = ChatPromptTemplate.from_template("""
                        You are a senior interviewer. Analyze the following question and the candidate's answer.
                        You must provide a score from 0-10 along with concise, constructive feedback.
                        
                        Question: {question}
                        Candidate's Answer: {answer}
                        
                        Feedback (with score and improvement points):
                        """)
                        
                        feedback_chain = feedback_prompt | llm | StrOutputParser()
                        feedback = feedback_chain.invoke({"question": questions[current_q], "answer": user_answer})
                        
                        # Save the answer and feedback
                        st.session_state.answers.append(user_answer)
                        st.session_state.feedback.append(feedback)
                        st.session_state.current_q += 1
                        
                        st.rerun()
                else:
                    st.warning("⚠️ Please type an answer.")
        
        with col2:
            if st.button("⏹️ End Interview", key=f"end_{current_q}"):
                st.session_state.interview_complete = True
                st.rerun()
    
    else:
        # All questions completed
        st.session_state.interview_complete = True
        st.rerun()

# --- Interview Completion Report ---
if st.session_state.interview_complete:
    st.balloons()
    st.header("🎉 Interview Complete!")
    st.subheader("📊 Your Performance Report")
    
    for i, (q, a, f) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedback)):
        with st.expander(f"Question {i+1}: {q[:50]}..."):
            st.write(f"**Your Answer:** {a}")
            st.write(f"**Feedback:** {f}")
    
    if st.button("🔄 Practice Again"):
        for key in ['questions', 'current_q', 'answers', 'feedback', 'interview_active', 'interview_complete']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("🚀 AI Interview Coach - Sharpen Your Skills!")
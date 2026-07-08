# 🚀 AI Interview Coach - Professional Project Report

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features & Functionality](#features--functionality)
3. [Technical Requirements](#technical-requirements)
4. [Project Architecture](#project-architecture)
5. [Project Structure](#project-structure)
6. [User Interface (UI) Walkthrough](#user-interface-ui-walkthrough)
7. [Troubleshooting & Errors Resolved](#troubleshooting--errors-resolved)
8. [Future Enhancements](#future-enhancements)
9. [Conclusion](#conclusion)

---

## 📌 Project Overview

**Project Name:** AI Interview Coach  
**Developer:** Aqsa Rasheed  
**GitHub Repository:** [https://github.com/aqsarasheed234234-ai/Interview-Coach-Project](https://github.com/aqsarasheed234234-ai/Interview-Coach-Project)

### 🎯 Objective
The **AI Interview Coach** is a web-based application designed to help job seekers practice technical interviews. The system uses a Large Language Model (LLM) to generate customized interview questions based on the user's role and skills, evaluate their answers, and provide constructive feedback with a score.

### 🔧 Technologies Used
| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **Streamlit** | Web application framework for UI |
| **LangChain** | Framework for building LLM-powered applications |
| **Groq API** | LLM provider (Llama 3.3 70B) |
| **PyPDF2** | PDF parsing and text extraction |
| **Python-dotenv** | Environment variable management |
| **Git/GitHub** | Version control and code hosting |

---

## ✨ Features & Functionality

### 1️⃣ User Profile Management
- **Input Fields:**
  - User Name (text input)
  - Job Title / Role (e.g., Data Scientist, MERN Developer)
  - Tech Stack / Skills (comma-separated list)
  - **OR** Upload CV (PDF format) – automatically extracts skills

### 2️⃣ AI-Powered Question Generation
- The system calls the **Groq API (Llama 3.3 70B)** to generate **exactly 5 unique** technical questions.
- Questions are tailored to the user's:
  - Job Role
  - Skills/Tech Stack
  - CV content (if uploaded)

### 3️⃣ Interactive Interview Session
- Each question is displayed one at a time.
- User types their answer in a text area.
- **Submit Answer:** AI analyzes the answer and provides:
  - **Score (0-10)**
  - **Constructive Feedback** (improvement points)
- The process repeats for all 5 questions.

### 4️⃣ Final Performance Report
- After completing all questions, a comprehensive report is generated.
- **Summary:**
  - All questions with user answers
  - AI-generated feedback for each answer
  - Balloon animation for celebration 🎈

### 5️⃣ Sidebar Interface
- User profile inputs are placed in the sidebar for a clean layout.
- **"Start Interview"** button triggers the entire workflow.

---

## 🛠️ Technical Requirements

### 📦 Required Python Packages

---

# 📄 Chat with PDF Documents (Streamlit App)

This project is a **Streamlit-based application** that allows users to chat with PDF documents using an LLM powered by **Groq** and PDF parsing via **LlamaParse**.

---

##  Prerequisites

Make sure you have the following installed:

* **Python 3.9 or newer**
* **pip** (Python package installer)

---

##  Setup and Installation

Follow these steps to set up and run the project locally.

---

### 🔹 Step 1: Set Up the Virtual Environment

After unzipping the project folder, navigate into it using your terminal:

```bash
cd /path/to/project-folder
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment (Windows):

```bash
.\venv\Scripts\activate
```

> You should see `(venv)` in your terminal once it’s activated.

---

### 🔹 Step 2: Install Required Packages

With the virtual environment active, install the dependencies:

```bash
pip install -r requirements.txt
```

---

### 🔹 Step 3: Obtain API Keys

This application requires **two API keys**.

#### 1️⃣ Groq API Key (LLM)

* **Website:** [https://console.groq.com/](https://console.groq.com/)
* **Steps:**

  1. Sign up for a free account.
  2. Go to **API Keys** in the left-hand menu.
  3. Click **Create API Key** and give it a name.
  4. Copy the key (starts with `gsk_...`).

---

#### 2️⃣ LlamaParse API Key (PDF Parsing)

* **Website:** [https://cloud.llama.com/](https://cloud.llama.com/)
* **Steps:**

  1. Sign up for a free account.
  2. Navigate to **API Keys**.
  3. Click **Create API Key** and give it a name.
  4. Copy the key (starts with `llm-...`).

---

### 🔹 Step 4: Create the `.env` File

In the **main project folder** (where `streamlit_app.py` is located), create a file named `.env`.

Add your API keys in the following format:

```env
GROQ_API_KEY="paste-your-groq-key-here"
LLAMA_PARSE_KEY="paste-your-llamaparse-key-here"
```

Save and close the file.
The application will automatically load these keys.

---

## ▶️ Running the Application

With the virtual environment still active, run:

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your default browser at:

```
http://localhost:8501
```

---

## 💬 How to Use the App

### 📌 Chat with a Document

1. Use the **sidebar** to:

   * Load the example `NVIDIAAn.pdf`, **or**
   * Upload your own PDF file.

2. Select the document from the **“Which document should we chat about?”** dropdown.

3. Ask questions in the **chat box** at the bottom of the page.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Groq API**
* **LlamaParse**

---



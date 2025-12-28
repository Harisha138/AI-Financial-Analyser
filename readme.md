Prerequisites:
* Python 3.9 or newer
* `pip` (Python package installer)
Setup and Installation Instructions
Here are the step-by-step instructions to set up and run this project locally.
Step 1: Set Up the Virtual Environment
After unzipping the project folder, navigate into it using your terminal:
cd /path/to/project-folder
Create a Python virtual environment to manage dependencies:
python -m venv venv
.\venv\Scripts\activate
Step 2: Install Required Packages
With the virtual environment active, install all required libraries from the
requirements.txt file:
pip install -r requirements.txt
Step 3: Obtain API Keys

This application requires two API keys to function.
1. Groq API Key (for the LLM)
o Website: https://console.groq.com/
o Instructions:
1. Sign up for a free account.
2. Navigate to the "API Keys" section in the left-hand menu.
3. Click "Create API Key" and give it a name.
4. Copy the key that starts with gsk_....
o Screenshot Guide:
2. LlamaParse API Key (for parsing PDFs)
o Website: https://cloud.llama.com/
o Instructions:
1. Sign up for a free account.
2. Navigate to the "API Keys" section.
3. Click "Create API Key" and give it a name.
4. Copy the key that starts with llm-....
o Screenshot Guide:
Step 4: Create the .env File
In the main project folder (the same place streamlit_app.py is located), create a new file named
.env.
Open this .env file in a text editor and paste your two API keys in the following format:
GROQ_API_KEY="paste-your-groq-key-here"
LLAMA_PARSE_KEY="paste-your-llamaparse-key-here"
Save and close the file. The application will automatically load these keys.
Running the Application
With your virtual environment still active (you see (venv) in your terminal), run the following
command:
Bash
streamlit run streamlit_app.py
This will automatically open the application in your default web browser (at an address like
http://localhost:8501).
How to Use the App
1. Chat with a Doc:
o Use the sidebar to load the example "NVIDIAAn.pdf" file.
o Or, upload your own PDF documents.

o Select the document you wish to chat with from the "Which document should
we chat about?" dropdown.
o Ask questions in the chat box at the bottom.

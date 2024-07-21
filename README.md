## Python Question-Answering System with LangChain and Google Gemini

This project implements a document-based question-answering system using LangChain, Google Gemini, and Chroma. The system allows users to ask questions about a set of documents and receive accurate and relevant answers.

### Project Structure

The project is divided into two main parts:

1. **Database Generation (Jupyter Notebook):**
   - A Jupyter notebook (`qa_application.ipynb`) is responsible for loading, processing, and indexing the source documents.
   - Documents are loaded from the file system.
   - The `langchain_community.document_loaders.generic` library provides the functionality to load documents.
   - Documents are divided into smaller chunks to facilitate processing.
   - Embeddings are generated for each chunk using the `GoogleGenerativeAIEmbeddings` model.
   - Embeddings and text chunks are stored in a vector database using the `Chroma` library.

2. **Web Application (FastAPI):**
   - A FastAPI server exposes a WebSocket endpoint for user interaction.
   - Users can connect to the server via WebSocket and submit questions.
   - Received messages are processed by the `QAApplication` class.
   - The `QAApplication` class loads the Chroma database and initializes the information retrieval chain.
   - The retrieval chain uses the Google Gemini language model (`gemini-1.5-flash`) to understand questions and retrieve relevant information from the database.
   - Answers are sent back to the user via WebSocket.

### Main Files

- `notebooks/qa_application.ipynb`: Jupyter notebook for generating the Chroma database.
- `src/main.py`: Main FastAPI application file.
- `src/utils/`: Directory containing auxiliary modules.
    - `qa_application.py`: Defines the `QAApplication` class.
    - `index.py`: Contains the function to load the user interface HTML.
- `src/data/chroma.sqlite3`: The Chroma database file.
- `.env`: File to store environment variables (e.g., API key).

### How to Run

1. **Generate the Database:**
   - Navigate to the `notebooks` directory in the terminal: `cd notebooks`
   - Open and run the `qa_application.ipynb` Jupyter notebook to create the Chroma database.
   - Ensure to specify the correct path to the source documents within the notebook.

2. **Set Environment Variables:**
   - Create a `.env` file at the root of the project (parent directory of `src`).
   - Define the following environment variables in the `.env` file:
     - `GOOGLE_API_KEY`: Your Google Cloud API key.
     - `PERSIST_DIRECTORY`: Path to the directory where the Chroma database will be stored. **Make sure this path is accessible from within the `src` directory.**

3. **Install Dependencies:**
   - Ensure you are in the project's root directory. 
   - Execute the following command to install the dependencies:

     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application:**
   - Make sure you are in the project's root directory.
   - Run the following command to start the FastAPI server:

     ```bash
     uvicorn src.main:app --reload
     ```

5. **Access the Application:**
   - Open a web browser and go to `http://127.0.0.1:8000/`.

### How to Use the Application

1. **Access the Interface:** Open your web browser and navigate to `http://127.0.0.1:8000/`. You will see a simple chat interface.
2. **Type your Question:** Type your question in the text box at the bottom of the page and click "Send".
3. **View the Answer:** The system's response will be displayed in the chat area above the text box. 

### Notes

- The `GoogleGenerativeAIEmbeddings` model requires a Google Cloud API key.
- Application performance depends on database size and machine processing power.
- The code includes comments explaining key steps and functionalities.

### Future Improvements

- Implement authentication and authorization to restrict access to the application.
- Allow users to upload their own documents.
- Add support for different file types (e.g., PDF, Word).
- Improve the user interface. 

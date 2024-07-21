import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

class QAApplication:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QAApplication, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        load_dotenv()
        
        self.PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.db = Chroma(persist_directory=self.PERSIST_DIRECTORY, embedding_function=self.embeddings)
        self.retriever = self.db.as_retriever(
            search_type="mmr",  # Uses the "Maximal Marginal Relevance" search method
            search_kwargs={"k": 8},  # Returns the 8 most relevant documents
        )

        # Initialize the Google Generative AI language model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Specifies the model to be used
            temperature=0,  # Controls the randomness of the response (0 = less random)
            top_k=10,  # Considers the top 10 responses during generation
            # Safety settings for the model
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        # Define the prompts
        self.init_prompts()

        # Create the chains
        self.retriever_chain = create_history_aware_retriever(self.llm, self.retriever, self.search_prompt)
        self.document_chain = create_stuff_documents_chain(self.llm, self.answer_prompt)
        self.qa_chain = create_retrieval_chain(self.retriever_chain, self.document_chain)

    def init_prompts(self):
        # Prompt to generate the search query based on the conversation history
        self.search_prompt = ChatPromptTemplate.from_messages(
            [
                ("placeholder", "{chat_history}"),  # Includes the conversation history
                ("user", "{input}"),  # Includes the user's question
                (
                    "user",
                    "Given the above conversation, generate a search query to look up information relevant to the conversation",
                ),  # Instruction to generate the query
            ]
        )

        # Prompt for the language model to answer the question
        self.answer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Answer the user's questions based on the below context:\n\n{context}",
                ),  # Instruction for the model
                ("placeholder", "{chat_history}"),  # Includes the conversation history
                ("user", "{input}"),  # Includes the user's question
            ]
        )

    def get_qa_chain(self):
        return self.qa_chain

# Usage
qa_app = QAApplication()
qa_chain = qa_app.get_qa_chain()
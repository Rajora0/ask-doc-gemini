import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils.qa_application import QAApplication  
from utils.index import get_html  

app = FastAPI()

qa_app = QAApplication()  # Instantiate the QAApplication class
qa_chain = qa_app.get_qa_chain()  # Get the QA chain

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=get_html())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            # Use the QAApplication class to process the message
            answer = qa_chain.invoke({"input": data['message']})['answer']

            response = {
                "username": "AI",
                "message": answer
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("WebSocket connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

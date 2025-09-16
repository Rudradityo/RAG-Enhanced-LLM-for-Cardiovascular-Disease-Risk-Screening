from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rag_prompt

# Create an instance of FastAPI class
app = FastAPI()

'''
Define a Pydantic Model named QueryRequest that inherits from BaseModel
Specify that query must be of type string
'''
class QueryRequest(BaseModel):
    query: str


'''
Handle POST requests sent to /process/ endpoint
Asynchronous function allows for non-blocking operations, enabling the program to handle other tasks while waiting for operations like I/O-bound processes to complete
QueryRequest is a Pydantic model that defines the structure and data types of the request data
The parameter request is an instance of QueryRequest Pydantic Model
Accessing request.query retrieves the value of the query attribute defined in that model
'''
@app.post("/process/")
async def get_model_response(request: QueryRequest):
    try:
        
        print(f"Patient Case Data in api.py:\n{request.query}\n")
        
        response = rag_prompt.create_prompt(request.query)
        
        print(f"Response to be displayed to user in api.py:\n{response}")
        
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
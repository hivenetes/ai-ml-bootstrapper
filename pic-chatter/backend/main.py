from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Define the origins that are allowed to make requests
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # Alternate localhost
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to PicChatter!"}

@app.get("/get_image_description/{image_filename}/{query}")
def get_image_description(image_filename: str, query: str):

    image_url = os.getenv("SPACES_ENDPOINT") + image_filename

    #Upload the image to the space  
    url = os.getenv("API_URL")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("BEARER_TOKEN")
    }
    data = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": query
                    }
                ]
            }
        ],
        "max_tokens": 600,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return {"description": content}
    else:
        return {"error": "Failed to get image description", "status_code": response.status_code}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    
import uvicorn
from fast import app

if __name__ == "__main__":
    uvicorn.run(
        "server:app",  # Import string for the application
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enables reloading of the server on code changes
        workers=4,    # Number of worker processes
    )
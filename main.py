import uvicorn
import os

if __name__ == '__main__':
  uvicorn.run("src.app:app", host="0.0.0.0", port=4000, reload=True)
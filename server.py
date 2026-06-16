import os
import sys
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "server")

if MODULE_DIR not in sys.path:
	sys.path.insert(0, MODULE_DIR)

from main import app

if __name__ == "__main__":
	uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)
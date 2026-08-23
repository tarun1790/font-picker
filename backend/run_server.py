import os
import sys
import asyncio
import traceback

# Append current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn

if __name__ == "__main__":
    print("[SERVER RUNNER] Starting server execution...")
    try:
        config = uvicorn.Config(
            "backend.app:app", 
            host="127.0.0.1", 
            port=8000, 
            log_level="info",
            loop="asyncio"
        )
        server = uvicorn.Server(config)
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("[SERVER RUNNER] Server stopped gracefully by KeyboardInterrupt.")
    except Exception as e:
        print(f"[SERVER RUNNER] Unexpected exception: {e}")
        traceback.print_exc()

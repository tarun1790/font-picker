import os
import sys
import asyncio
import traceback
import time

# Append current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn

if __name__ == "__main__":
    print("[SERVER RUNNER] Starting server execution...")
    try:
        sys.stdin = open(os.devnull, 'r')
    except Exception:
        pass

    while True:
        try:
            uvicorn.run(
                "backend.app:app", 
                host="127.0.0.1", 
                port=8008, 
                log_level="info",
                loop="asyncio"
            )
        except KeyboardInterrupt:
            print("[SERVER RUNNER] Server stopped gracefully by KeyboardInterrupt.")
            break
        except Exception as e:
            print(f"[SERVER RUNNER] Exception in server loop, restarting in 2s: {e}")
            traceback.print_exc()
            time.sleep(2)

import os
import sys
import asyncio
import traceback

# Append current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn

if __name__ == "__main__":
    print("[SERVER RUNNER] Starting server execution...")
    while True:
        try:
            config = uvicorn.Config(
                "backend.app:app", 
                host="127.0.0.1", 
                port=8000, 
                log_level="info",
                loop="asyncio",
                install_signal_handlers=False
            )
            server = uvicorn.Server(config)
            asyncio.run(server.serve())
        except KeyboardInterrupt:
            print("[SERVER RUNNER] Server stopped gracefully by KeyboardInterrupt.")
            break
        except Exception as e:
            print(f"[SERVER RUNNER] Exception in server loop, restarting in 2s: {e}")
            traceback.print_exc()
            import time
            time.sleep(2)

import os
import sys

# Append current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
import traceback

if __name__ == "__main__":
    print("[SERVER RUNNER] Starting server execution...")
    try:
        uvicorn.run(
            "backend.app:app", 
            host="127.0.0.1", 
            port=8000, 
            log_level="info",
            workers=1
        )
    except KeyboardInterrupt:
        print("[SERVER RUNNER] Server stopped gracefully by KeyboardInterrupt.")
        sys.exit(0)
    except SystemExit:
        print("[SERVER RUNNER] Server received SystemExit signal.")
        sys.exit(0)
    except Exception as e:
        print(f"[SERVER RUNNER] Unexpected exception: {e}")
        traceback.print_exc()
        sys.exit(1)

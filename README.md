# Font DNA Evolution & 3D Interactive Packaging Simulator

An agentic CAD design suite that allows designers and brands to scan packaging wrappers, edit visual bounding boxes in 2D, and immediately preview layout overlays on realistic 3D containers in crystal clear 2K resolution.

---

## 🚀 Key Features

* **Coordinated 2D-to-3D Packaging Canvas**: Drag, resize, edit text, or add custom bounding boxes on a 2D layout editor, and watch the text elements slide and scale on the 3D WebGL container in real-time.
* **3D Multi-Face Editor**: Swap between designing the **Front**, **Back**, **Sides**, **Bottom**, and **Top** folds of packaging boxes, jars, or bottles.
* **3D Multi-Shape Profiles**: Switch between different package geometries dynamically:
  * 📦 **Box**: Rectangular slab (ideal for chocolate, soap boxes).
  * 🥫 **Jar / Canister**: Cylinder wrapper (ideal for coffee tins, tea jars).
  * 🍾 **Bottle**: Composite shape with main body cylinder, tapered neck, and cap.
  * ⬡ **Hex Prism**: Hexagonal packaging box.
  * 💊 **Vial / Tin**: Short cosmetic vial tin.
* **2K Quad-HD Render Quality**: Textures render at high-density `2048x2048` pixel resolution, backed by hardware-maximized anisotropic filtering to eliminate graphical tilt blur.
* **AI Typography Router**: Zero-shot categorization models and FAISS vector indices recommend Google Fonts matching target consumer emotions.

---

## 🛠️ Local Installation & Setup

Ensure you have **Node.js (v18+)** and **Python (v3.8+)** installed.

### 1. Backend Server Setup

The backend FastAPI service hosts the zero-shot classifier, FAISS vector index, and Cypher knowledge graph traversal.

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (automatically sets up PyTorch with GPU/CUDA acceleration if supported)
pip install -r requirements.txt

# Run the FastAPI server
python run_server.py
```
The backend server runs on `http://127.0.0.1:8000`.

### 2. Frontend Web Client Setup

The frontend Vite client hosts the Interactive WebGL container viewer and the 2D Visual OCR editor.

```bash
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Run the Vite development server
npm run dev
```
Open **`http://localhost:5173/`** in your browser.

---

## 📤 How to Share the Project

The codebase has been configured and pushed to a remote GitHub repository. To share this project with a client, colleague, or developer:

1. **Send the GitHub link**:
   [https://github.com/tarun1790/font-picker](https://github.com/tarun1790/font-picker)
2. **Collaborator Access**:
   Ensure they clone the repository:
   ```bash
   git clone https://github.com/tarun1790/font-picker.git
   ```
3. **Execution**:
   They can follow the steps in this `README.md` to run both the FastAPI backend and the React frontend on their local machine.

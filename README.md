# English Learning Web App

This is a modern web application version of the `random_generator.py` script, featuring a **React** frontend and a **FastAPI** (Python) backend.

## 🚀 How to Run

### 1. Simple Way (Windows)
Double-click the `run.bat` file in the `web_app` directory. This will:
- Open a terminal for the **Python Backend**.
- Open a terminal for the **React Frontend**.
- You can then visit `http://localhost:5173` in your browser.

### 2. Manual Way
If you prefer running them manually:

## 🌍 Cloud Deployment (Monorepo Instructions)

Since this project has both a `backend` and `frontend`, you must configure the **Root Directory** for each service:

### **Backend (Railway.app)**
1. Connect your repo.
2. Ensure **Root Directory** is empty (or set to `/`).
3. Railway will automatically detect the **Dockerfile** and build the entire monorepo correctly.
4. Set the **Environment Variable** `PORT` to `8000` (optional, Railway handles this automatically).

### **Frontend (Vercel)**
1. Connect your repo.
2. During setup, look for **Root Directory**.
3. Click **Edit** and select the `frontend` folder.
4. Set the **Environment Variable** `VITE_API_URL` to your Railway URL.

---

#### **Backend (Local)**
1. Open a terminal in `web_app/backend`.
2. Run: `python main.py`
3. The API will be available at `http://localhost:8000`.

#### **Frontend**
1. Open a terminal in `web_app/frontend`.
2. Run: `npm run dev`
3. The app will be available at `http://localhost:5173`.

## 🛠️ Requirements
- **Python 3.7+**
- **Node.js** (for React)
- Libraries: `fastapi`, `uvicorn`, `requests`, `beautifulsoup4`
- Frontend dependencies: Installed automatically via Vite scaffolding.

## ✨ Features
- **Random Word Explorer**: Fetch and display meanings, synonyms, and examples.
- **Visual Context**: Related images from Yahoo Images.
- **Pronunciation Coach**: Integrated YouGlish widget with nearby words.
- **Modern UI**: Dark/Light mode support with a premium aesthetic.

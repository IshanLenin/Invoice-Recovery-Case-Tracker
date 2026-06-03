# Invoice Recovery Dashboard (Full-Stack)

A full-stack invoice recovery and client management system. Built with a FastAPI/PostgreSQL backend and a React (Vite) frontend.

## 🚀 Architecture
* **Backend:** FastAPI, Python 3.10+, PostgreSQL, SQLAlchemy, JWT Authentication
* **Frontend:** React, Node.js, Vite

## 📁 Project Structure
* `/backend` - Contains the Python FastAPI server and database configurations.
* `/frontend` - Contains the React user interface.

## 🛠️ Prerequisites
Before running this project, ensure you have the following installed on your machine:
* **Python 3.10+**
* **Node.js** (LTS version)
* **PostgreSQL** (Running locally)

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/IshanLenin/Invoice-Recovery-Case-Tracker
cd Invoice-Recovery-Project
```

### 2. Database configuration
Create an .env file inside the /backend folder and match the postgres details to match the one in your local machine.
```plaintext
DATABASE_URL="postgresql://<username>:<password>@localhost:5432/primetrade_db"
```

### 3. Start the backend
```bash
cd backend
```

Activate the virtual environment
```bash
# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and start the server
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```


### 4. Start the frontend
```bash
cd frontend
```

### 5. Start the node dependencies and start the frontend server.
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

***
###💡Features

Client Management: Create and view debtor profiles.

Case Management: Create and track invoice recovery cases linked to specific clients.

CORS Configured: Backend and frontend communicate seamlessly across local ports
***

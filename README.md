<div align="center">
  
# Uni AI Bias Detection Tool
**A tool to detect bias from AI career guidance feedback to students CVs | Backed by IBM & Lenovo, for the Responsible AI Consortium (RAIC).**

</div>

## Running The Project

### Frontend Setup
1) Make sure NodeJS is installed (check if installed via `node -v` in the CLI), can be installed here:  https://nodejs.org/en/ 
2) In the `frontend` folder, run `npm install`
3) Also in the `frontend` folder, run `npm run dev`
4) Open the localhost link, and everything should be working!

### Backend Setup
1) `cd` into backend folder
2) Create a python 3.12 `venv` and activate it: `py -3.12 -m venv venv` then `.\venv\Scripts\Activate.ps1` or `.\venv\bin\activate`
3) Install the reqs in requirements.txt `pip install -r requirements.txt`
4) Add `env` file to the `backend` folder
5) Run `python -m BiasAI.main` and everything should be working
6) `uvicorn app:app --reload --port 8000` Starts the backend connection

To run the auto-formatter, just run `black .` and the files will be auto-formatted to best practices.

## Mockups
<img width="600" height="450" alt="Frame 2" src="https://github.com/user-attachments/assets/a1130409-c2af-4899-9381-445a47699e5a" />
<img width="600" height="450" alt="Frame 3" src="https://github.com/user-attachments/assets/7807af8e-279f-41a7-99dc-f0f1012de98c" />

## Tech Stack
### Frontend
- Tailwind CSS
- HTML
- React
- TypeScript
- Vite + Node.js

### Backend
- Python + FastAPI
- Black formatter
- Claude API
- Vercel (Deployment)

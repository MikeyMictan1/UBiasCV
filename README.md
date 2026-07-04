<div align="center">
  
# UBiasCV
**A tool that detects Gender Bias from AI CV Feedback | Backed by IBM & Lenovo, for the Responsible AI Consortium (RAIC).**

<img width="560" height="450" alt="image" src="https://github.com/user-attachments/assets/5e9a18f0-652e-47f9-abc8-f65db5e0882d" />

</div>

## Using The Tool
### 1) User: Select your purpose for using the tool
<img width="1110" height="286" alt="image" src="https://github.com/user-attachments/assets/a539f662-66ce-423b-8e61-5e6ce68bec0c" />

### 2) Input a CV and AI generated feedback about that CV, as well as answering context questions
<img width="1118" height="711" alt="image" src="https://github.com/user-attachments/assets/a6e46a30-c629-4905-a403-91891d3cb06b" />

### 3) Generate and review the Gender Bias Report
<img width="1185" height="729" alt="image" src="https://github.com/user-attachments/assets/c71ddc92-ee03-4cc4-81be-c565669e2115" />



## Running The Project (Developers)

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

### RBA Strategy Testing
1) Place CVs and feedback in the `backend/StrategyTesting/SampleCVFeedback` folder, with the naming convention: `testXgender.pdf` for CVs and `testXgender_feedback.txt` for feedback. Replace 'X' and 'gender' with the name of the test and gender.
2) `cd backend` and run `python -m StrategyTesting.rba_tester` to run the strategy tester.

To run the auto-formatter, just run `black .` and the files will be auto-formatted to best practices.

## Architecture
<img width="2019" height="1419" alt="raic (2)" src="https://github.com/user-attachments/assets/f512f225-8bd3-4d71-a373-ecf3c2291b3f" />



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

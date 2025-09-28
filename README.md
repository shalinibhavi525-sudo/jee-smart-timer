# JEE Smart Timer 

A web-based timer + analytics tool I built to track my JEE question practice.  
It logs how long each question takes, whether I solved it correctly,  
and then shows performance stats + graphs in the browser.

---

## Features
- Start/stop timer per question
- Log correctness (correct/wrong)
- Stores results in `data/sessions.csv`
- Shows:
  - Average time per question
  - Accuracy percentage
  - Graph of times vs questions (auto-generated)

---

## Installation
```bash
git clone https://github.com/your-username/jee-smart-timer-web.git
python main.py
http://127.0.0.1:5000/
cd jee-smart-timer-web
pip install -r requirements.txt

# 🛡️ AI Defending AI — Prompt Injection Firewall

A live demonstration of an AI system defending itself against adversarial prompt injection and jailbreak attacks — in real time.

## 🎯 The Problem
As companies rush to deploy LLM-powered chatbots, most have no defense against **prompt injection** — attackers tricking an AI into leaking secrets, ignoring its rules, or acting outside its intended scope. This project builds, attacks, and defends a real AI system to measure exactly how vulnerable (and defensible) these systems really are.

## 🧩 How It Works

1. **Victim AI** (`victim_app.py`) — a customer support chatbot holding a secret it must never reveal.
2. **Attacker** (`attacker.py`) — automatically fires 10+ real-world jailbreak techniques at it (roleplay tricks, fake authority claims, instruction leaks, encoding tricks, etc).
3. **Firewall** (`firewall.py`) — a two-layer defense: scans messages *before* they reach the AI, and scans replies *after*, redacting any leak that slips through.
4. **Secure App** (`secure_app.py`) — the protected version of the chatbot, logging every interaction.
5. **Dashboard** (`dashboard.py`) — a live Streamlit dashboard visualizing attack outcomes and defense rate.

## 📊 Results

| Version | Defense Rate |
|---|---|
| Unprotected AI | 90% (1 leak via "Instruction Leak" attack) |
| With Firewall | **100%** (0 leaks across 10+ attack types) |

## 🖥️ Tech Stack
Python · FastAPI · Groq (Llama 3.3) · Streamlit · Plotly · Regex-based pattern detection

## 🚀 Run It Yourself

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-defending-ai.git
cd ai-defending-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your free Groq API key to a .env file
echo GROQ_API_KEY=your_key_here > .env

# 5. Run the secure app
uvicorn secure_app:app --reload --port 8001

# 6. In a new terminal, run the attacker
python attacker.py

# 7. In another terminal, launch the dashboard
streamlit run dashboard.py
```

## 🔮 Future Improvements
- Replace regex rules with a trained ML classifier for attack detection
- Add rate-limiting and IP-based anomaly detection
- Expand attack library with real-world jailbreak datasets
- Add a second LLM as an independent "judge" to review flagged messages

## 📌 Why This Matters
This isn't a toy chatbot — it's a working demonstration of the exact vulnerability class (prompt injection) currently listed in the **OWASP Top 10 for LLM Applications**. Every company deploying an LLM in production faces this problem today.

---
Built as part of an ongoing exploration into AI safety and adversarial ML.
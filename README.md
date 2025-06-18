# 📊 Customer Journey Risk Radar

> **A strategic AI pipeline to uncover customer pain points from public data sources such as Reddit, Twitter, Google Play, App Store or YouTube — mapped across the OTT customer journey.**

---

## 🧠 What This Project Solves

Traditional customer journey analytics rely on internal data (e.g. app usage, support tickets). But in reality, customers leave rich feedback on public platforms like Reddit, app reviews, or X. These external signals are often:
- Unfiltered
- Early warning indicators
- Missed by product teams

This project builds an end-to-end AI pipeline to uncover these **external pain points**, align them to defined **customer journey stages**, and extract actionable **insights for strategic decision-making**.

---

## 🎯 Use Case: OTT Platforms

OTT (Over-the-top) platforms like Netflix, Disney+, or local streaming apps are ideal for this project because:
- Their user journey is well-defined (Signup → Onboarding → Content Discovery → Streaming → Billing → Churn)
- Public feedback is abundant
- Churn risk is high and sensitive to friction

---
## ⚙️ Tools & Technologies

| Layer            | Tool/Library                            |
|------------------|-----------------------------------------|
| Data Source      | Reddit JSON export (via PRAW/scraping) |
| Preprocessing    | Python, YAML, VADER                     |
| Classification   | LangChain + DeepSeek (OpenRouter)      |
| Keyword Extraction | KeyBERT + Sentence Transformers      |
| Visualization    | Streamlit                              |

---

## 🧪 Pipeline Steps

### 1. Define Journey Stages (YAML)
```yaml
tasks:
  - stage: Signup
    description: User registration and login issues
    examples:
      - I can’t log in
      - Signup page won’t load
  ...
```

### 2. Classify Reddit Posts
- Each post is assigned to a stage using **few-shot prompting** with `deepseek-chat-v3-0324:free` model
- The sentiment score is calculated with VADER

### 3. Extract Pain Points with KeyBERT
- Only negative posts are analyzed
- Top phrases are extracted per stage

### 4. Visualize with Streamlit
- Filter by stage
- View top pain point keywords + sentiment distribution

---

## 📂 Folder Structure

```
📦 customer-journey-risk-radar
├── data/
│   └── classified_reddit.json
├── prompts/
│   └── tasks.yaml
├── stage_classifier_openrouter.py
├── keyword_analysis.py
├── dashboard.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## 📌 Strategic Value

- **External Signal Mining**: Taps into unfiltered customer voice from public platforms
- **Journey-Aware Feedback**: Feedback is contextually linked to where users struggle
- **Actionable Dashboards**: Built to serve product managers, CX, and strategy teams

---

## ✍️ Author
**Eser Saygın**  
Strategy & AI Portfolio  
[LinkedIn](https://linkedin.com/in/esersaygin)

---

## 📄 License
MIT

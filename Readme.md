### **Overview**

| Stage | Description |
|-------|--------------|
| **Data Sources** | PhiUSIIL + Crawled HTML / DOM |
| **Feature Extraction** | URL → `url_lexical_model.py`<br>HTML → `html_content_model.py`<br>DOM → `dom_content_model.py` |
| **Supervised Learning (SL)** | Logistic Regression / Ensemble baselines |
| **Reinforcement Learning (RL) Controller** | DDQN / Q-learning controller that selects which SL model to query (URL → HTML → DOM) |
| **Supervised Models** | URL (fast, low cost), HTML (content features), DOM (structural features) |
| **Decision Fusion Layer** | Weighted voting / RL policy integration |
| **Continual Learning Module** | Retrains SL models, updates RL controller, detects concept drift, prevents forgetting |
| **Final Decision Layer** | Phishing / Legitimate (unified cost-aware decision) |

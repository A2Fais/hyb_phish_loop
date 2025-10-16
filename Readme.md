                           ┌───────────────────────────────────────┐
                           │            Data Sources               │
                           │  (PhiUSIIL + Crawled HTML / DOM)      │
                           └───────────────────────────────────────┘
                                             │
                                             ▼
              ┌────────────────────────────────────────────────────────┐
              │         Multi-Modal Feature Extraction Pipeline         │
              │────────────────────────────────────────────────────────│
              │  URL Lexical Features   → url_lexical_model.py          │
              │  HTML Content Features  → html_content_model.py         │
              │  DOM Structural Features→ dom_content_model.py          │
              └────────────────────────────────────────────────────────┘
                                             │
                                             ▼
                    ┌──────────────────────────────────────────────┐
                    │     Initial Supervised Learning (SL) Stage   │
                    │ (Logistic Regression / Ensemble Baselines)   │
                    └──────────────────────────────────────────────┘
                                             │
                                             ▼
          ┌────────────────────────────────────────────────────────────────┐
          │     Reinforcement Learning Controller (DDQN / Q-learning)       │
          │────────────────────────────────────────────────────────────────│
          │ - Observes confidence, cost, and reward signals                 │
          │ - Dynamically selects which SL model to query next              │
          │   (URL → HTML → DOM)                                            │
          │ - Balances detection accuracy vs. feature extraction cost       │
          └────────────────────────────────────────────────────────────────┘
                            │ Decision based on policy π(a|s)
                            ▼
      ┌───────────────────────────────┬───────────────────────────────┬───────────────────────────────┐
      ▼                               ▼                               ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ URL Supervised Model │     │ HTML Supervised Model│     │ DOM Supervised Model │
│ (Fast, low cost)     │     │ (Content features)   │     │ (Structural features)│
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
      ▼                               ▼                               ▼
                 ┌────────────────────────────────────────────────────────┐
                 │        Combined Decision Fusion Layer                  │
                 │ (Weighted voting / RL policy integration)              │
                 └────────────────────────────────────────────────────────┘
                                             │
                                             ▼
                 ┌────────────────────────────────────────────────────────┐
                 │       Continual Learning & Adaptation Module           │
                 │────────────────────────────────────────────────────────│
                 │ - Periodically retrains SL models with new samples     │
                 │ - Updates RL controller via replay buffer              │
                 │ - Detects concept drift (new phishing behaviors)       │
                 │ - Prevents catastrophic forgetting                     │
                 └────────────────────────────────────────────────────────┘
                                             │
                                             ▼
                 ┌────────────────────────────────────────────────────────┐
                 │      Final Decision Layer: Phishing / Legitimate       │
                 │ (Unified cost-aware decision after continual updates)  │
                 └────────────────────────────────────────────────────────┘

# Cost-Aware Phishing RL

                  ┌────────────────────┐
                  │  URL Supervised SL │──┐
                  └────────────────────┘  │
                                           ▼
                             ┌──────────────────────────┐
                             │ Reinforcement Controller │
                             │ (DDQN / Q-learning)      │
                             └──────────────────────────┘
                                  │ Decision based on
                                  │ confidence threshold
               ┌──────────────────┴──────────────────┐
               ▼                                     ▼
    ┌────────────────────┐                 ┌────────────────────┐
    │ HTML Supervised SL │                 │ DOM Supervised SL  │
    └────────────────────┘                 └────────────────────┘
               ▼                                     ▼
                         Combined Decision → Phishing / Legitimate

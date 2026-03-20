📘 Project Description — Real-Time Crash Game Backend (Django + Kafka / Redpanda)

Title: Real-Time Crash Betting Game Backend (Django + Kafka / Redpanda)

Description:
A scalable, event-driven backend for a crash-style betting game inspired by Aviator, built with Django. Designed for real-time gameplay, high concurrency, and distributed processing using Kafka / Redpanda. The system decouples game event producers from multiple consumers that process critical events like bets, cashouts, and round outcomes independently.

All services run in Docker containers, making it easy to deploy and scale. Game events are also streamed to ClickHouse for analytics, and Grafana dashboards monitor system performance and gameplay metrics in real-time.


---

🔑 Key Features

Event-Driven Architecture: Game events are published to Kafka / Redpanda topics as immutable streams.

Django Backend: Handles authentication, wallet management, game engine, and WebSocket API for real-time client updates.

Decoupled Consumer Services: Multiple services (wallet, risk/fraud detection, analytics, notifications) operate independently.

Independent Offsets: Each service uses its own consumer group, ensuring all events are processed fully and independently.

Analytics & Monitoring: Events streamed to ClickHouse; dashboards in Grafana provide real-time insights.

Containerized Deployment: Entire system runs in Docker, including Django backend, Kafka / Redpanda, ClickHouse, and Grafana.

Scalable & Fault-Tolerant: Kafka / Redpanda handles high-throughput streams and ensures fault tolerance.



---

🧠 Core Kafka / Redpanda Topics

Topic	Description

game.round	Round lifecycle events (started, crashed)
game.bet	Player bet placements
game.multiplier	Real-time multiplier values
game.cashout	Player cashout events



---

👥 Consumer Services (Own Consumer Groups)

Service	Responsibility

Wallet Service	Deducts player funds and credits winnings
Risk/Fraud Service	Detects suspicious or bot-like activity
Analytics Service	Streams data to ClickHouse for dashboards
Notification Service	Sends SMS / email / push notifications
WebSocket Gateway	Pushes live events to clients for real-time updates


> Each consumer group tracks its own offsets independently. Services can process events at their own pace without interfering with each other.




---

Example Event (JSON)

Bet Event

{
  "round_id": "83421",
  "user_id": 92,
  "bet_amount": 5,
  "timestamp": "2026-03-17T12:23:45Z"
}

Cashout Event

{
  "round_id": "83421",
  "user_id": 92,
  "multiplier": 2.37,
  "payout": 11.85
}


---

📊 Architecture Overview

┌───────────────┐
                   │  Django Game  │
                   │   Engine &    │
                   │  WebSocket    │
                   └──────┬────────┘
                          │ Publishes events
                          ▼
                   ┌───────────────┐
                   │ Kafka /       │
                   │ Redpanda      │
                   └──────┬────────┘
        ┌───────────────┼───────────────┐
        │               │               │
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ Wallet      │  │ Risk/Fraud   │  │ Analytics     │
│ Service     │  │ Service      │  │ Service       │
│ (Consumer   │  │ (Consumer    │  │ (Consumer)    │
│ Group)      │  │ Group)       │  │               │
└─────────────┘  └──────────────┘  └──────────────┘
       │                │                │
       ▼                ▼                ▼
   Ledger DB         Alerts / Logs     ClickHouse
                                          │
                                          ▼
                                      Grafana Dashboard

Everything runs in Docker containers.

Kafka / Redpanda handles the event streams.

ClickHouse collects analytics.

Grafana monitors metrics.



---

🛠 Tech Stack

Django – Backend + WebSocket server

Kafka / Redpanda – Event streaming

ClickHouse – Analytics / dashboards

Grafana – Monitoring & visualization

Docker – Containerized deployment






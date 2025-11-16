# 🌏 A2A Travel Planning System

Multi-Agent Travel Planning System using Agent-to-Agent (A2A) Protocol

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
uv sync
```

### 2. Cấu hình environment
Copy `.env.example` thành `.env` và điền API keys:
```bash
cp .env.example .env
```

Chỉnh sửa `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Chạy agents

**Terminal 1 - Weather Agent:**
```bash
uv run python -m agents.weather.agent
```

**Terminal 2 - Planning Agent:**
```bash
uv run python -m agents.planning.agent
```

**Terminal 3 - Coordinator:**
```bash
uv run python -m agents.coordinator.agent
```

Hoặc test với địa điểm tùy chỉnh:
```bash
uv run python -m agents.coordinator.agent "Paris" "Tokyo" "New York"
```

---

## 🧪 Testing với cURL

### Test Weather Agent (Port 5001)

**Lấy metadata:**
```bash
curl http://localhost:5001/a2a/.well-known/agent.json
```

**Lấy thời tiết:**
```bash
curl -X POST http://localhost:5001/a2a/tasks/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "role": "user",
      "content": {
        "type": "text",
        "text": "Hanoi"
      }
    }
  }'
```

### Test Planning Agent (Port 5002)

**Lấy metadata:**
```bash
curl http://localhost:5002/a2a/.well-known/agent.json
```

**Lấy activity suggestions:**
```bash
curl -X POST http://localhost:5002/a2a/tasks/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "role": "user",
      "content": {
        "type": "text",
        "text": "Plan for Da Nang with weather: Temperature: 28°C, Condition: Sunny, Humidity: 70%"
      }
    }
  }'
```

### Hoặc dùng test scripts

```bash
# Test tất cả agents
bash test_agents.sh

# Test riêng Weather Agent
bash test_weather.sh

# Test riêng Planning Agent với nhiều scenarios
bash test_planning.sh
```

---

## 📋 Kiến trúc hệ thống

### 🏗️ System Architecture

```mermaid
graph TB
    User[👤 User]
    
    subgraph "Coordinator Layer"
        Coord[🎯 Travel Coordinator<br/>Port 5003]
    end
    
    subgraph "Agent Layer"
        Weather[🌤️ Weather Agent<br/>Port 5001]
        Planning[🗺️ Planning Agent<br/>Port 5002]
    end
    
    subgraph "External Services"
        WeatherAPI[🌍 Weather API<br/>OpenWeather/Mock]
        Gemini[🤖 Google Gemini AI<br/>gemini-2.5-flash]
    end
    
    User -->|"Request:<br/>Location"| Coord
    Coord -->|"A2A Protocol<br/>send_message_async"| Weather
    Coord -->|"A2A Protocol<br/>send_message_async"| Planning
    Weather -->|"HTTP Request"| WeatherAPI
    Planning -->|"API Call"| Gemini
    
    Weather -->|"Response:<br/>Temperature, Condition"| Coord
    Planning -->|"Response:<br/>Activity Suggestions"| Coord
    Coord -->|"Combined Result"| User
    
    style User fill:#e1f5ff
    style Coord fill:#fff4e6
    style Weather fill:#e8f5e9
    style Planning fill:#f3e5f5
    style WeatherAPI fill:#fce4ec
    style Gemini fill:#fff3e0
```

### 🔄 Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Coordinator
    participant WeatherAgent
    participant PlanningAgent
    participant WeatherAPI
    participant GeminiAI

    User->>Coordinator: Request travel plan for "Hanoi"
    
    Note over Coordinator: Step 1: Get Weather Info
    Coordinator->>WeatherAgent: A2A Message: "Hanoi"
    WeatherAgent->>WeatherAPI: HTTP GET /weather?q=Hanoi
    WeatherAPI-->>WeatherAgent: Weather data (JSON)
    WeatherAgent-->>Coordinator: A2A Response: Temperature, Condition, Humidity
    
    Note over Coordinator: Step 2: Get Activities
    Coordinator->>PlanningAgent: A2A Message: "Plan for Hanoi with weather: 25°C, Sunny"
    PlanningAgent->>GeminiAI: Generate activities prompt
    GeminiAI-->>PlanningAgent: AI-generated activity suggestions
    PlanningAgent-->>Coordinator: A2A Response: Activity list
    
    Note over Coordinator: Step 3: Combine & Format
    Coordinator->>User: Complete travel plan:<br/>Weather + Activities
```

### 🔌 A2A Protocol Communication

```mermaid
graph LR
    subgraph "Message Flow"
        A[Client] -->|1. Create Message| B[A2AClient]
        B -->|2. HTTP POST<br/>/a2a/tasks/send| C[A2AServer]
        C -->|3. handle_message| D[Agent Logic]
        D -->|4. Process & Return| C
        C -->|5. HTTP Response| B
        B -->|6. Parse Response| A
    end
    
    style A fill:#bbdefb
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#ffccbc
```

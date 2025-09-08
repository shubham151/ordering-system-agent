# Drive Thru Ordering System

A modern AI-powered drive-thru ordering system that processes natural language requests to place, modify, and cancel food orders.

## Live Demo [https://ordering-system-agent.vercel.app/](https://ordering-system-agent.vercel.app/)  


## Features

- **Natural Language Processing**: Order using conversational language
- **Real-time Order Management**: Place, modify, and cancel orders instantly
- **AI-Powered**: Supports OpenAI GPT and Google Gemini models
- **Modern UI**: Clean, responsive interface built with SvelteKit
- **Backend**: FastAPI with clean architecture

## Tech Stack

### Frontend
- **SvelteKit** - Modern web framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Functional Programming** - Clean, testable code

### Backend
- **FastAPI** - Python web framework
- **Pydantic** - Data validation
- **OpenAI/Gemini APIs** - Natural language processing
- **Clean Architecture** - Separated concerns

## Usage Examples

### Placing Orders

```json
"I want 2 burgers and 3 fries"
"My friend and I each want a drink"
"Can I get one of everything?"
```

### Modifying Orders

```json
"Update my order 1 with 2 more burgers and no fries"
"Add 3 drinks to order 2"
"Remove all burgers from order 3"
```


### Canceling Orders

```json
"Cancel order 5"
"Please cancel my order #3"
```


## Local Development

### Prerequisites
- Node.js 18+
- Python 3.9+
- OpenAI API Key or Google Gemini API Key

### Backend Setup

1. **Clone and navigate**
   ```bash
   git clone https://github.com/shubham151/ordering-system-agent.git
   cd backend

2. **Create virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure environment**

    ```bash
    cp .env.template .env
    ```
5. **Run backend**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

### Frontend Setup

1. **Navigate to frontend**
    ```bash
    cd frontend
    ```

2. **Install dependencies**
    ```bash
    npm install
    ```

3. **Configure environment**
    ```bash
    PUBLIC_API_URL='http://localhost:8000'
    ```

4. **Run frontend**
    ```bash
    npm run dev
    ```
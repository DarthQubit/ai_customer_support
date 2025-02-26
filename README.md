# AI-Powered Customer Support Ticket Processing System

## Overview

This project implements an AI-powered system designed to process customer support tickets by classifying, prioritizing, and generating responses automatically. The system is built with modular, asynchronous agents that handle ticket analysis and response generation.

Bonus features include sentiment analysis and custom template creation via a large language model (LLM). Additionally, the system includes a relevancy check using an LLM-based approach to flag tickets that are out of scope (e.g., non-IT related inquiries).

---

## Project Structure

```
ai_customer_support/
├── agents/
│   ├── ticket_analysis_agent.py  # Analyzes tickets for categorization, priority, sentiment, and relevancy
│   ├── response_agent.py         # Generates responses based on ticket analysis
│   └── ticket_processor.py       # Orchestrates interactions between agents and maintains context
├── tests/
│   ├── test_ticket_analysis.py   # Unit tests for ticket analysis logic and edge cases
│   ├── test_response_agent.py    # Unit tests for response generation and custom template functionality
│   └── test_error_handling.py    # Tests error scenarios (e.g., invalid inputs, ambiguous requests)
├── app.py                        # Streamlit UI for interactive ticket processing
├── main.py                       # Command-line entry point for processing sample tickets
├── README.md                     # Project documentation
└── requirements.txt              # Lists all Python dependencies
```

---

## Setup Instructions

### Clone the Repository
```sh
git clone https://github.com/yourusername/ai_customer_support.git
cd ai_customer_support
```

### Create and Activate a Virtual Environment

#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

---

## Running the Application

### Command-Line Interface
Process sample tickets:
```sh
python main.py
```
This script processes sample tickets and prints out the ticket analysis and generated responses.

### Streamlit UI
Launch the UI:
```sh
streamlit run app.py
```
The UI includes fields for ticket details and customer information. It also offers an option to use a custom response template. Once submitted, the UI displays the ticket analysis (category, priority, key points, sentiment, etc.) and the generated response.

---

## Design Decisions

### Modular Agent Architecture
The system is divided into:
- **TicketAnalysisAgent**: Utilizes Hugging Face's zero-shot classification (e.g., `facebook/bart-large-mnli`) to categorize tickets and a sentiment-analysis pipeline (e.g., `distilbert-base-uncased-finetuned-sst-2-english`) to determine sentiment. It also employs an LLM-based approach to check for relevancy.
- **ResponseAgent**: Generates responses using a text-generation model (e.g., `distilgpt2`). Supports both predefined templates and custom template creation via a dedicated prompt.
- **TicketProcessor**: Acts as the orchestrator, maintaining context and coordinating interactions between the analysis and response agents.

### Asynchronous Processing
All major functions are asynchronous (`async def`), allowing for non-blocking I/O operations and setting a foundation for scaling the system to handle multiple tickets concurrently.

### Error Handling
The system includes comprehensive error handling to manage invalid inputs, API failures, and response quality issues. Exceptions are caught, and informative error messages are provided to ensure graceful degradation.

### Relevancy Check
An LLM-based method flags tickets as "irrelevant" if they do not fall within the domain (e.g., an out-of-scope inquiry such as a barista asking for coffee).

---

## Testing Approach

### Unit Testing
The `tests/` folder contains unit tests that cover:
- **Priority Assignment**: Ensuring that urgency keywords, customer roles, and business impact factors correctly affect the ticket's priority.
- **Response Generation**: Verifying template matching, personalization, and tone of the generated responses.
- **Error Handling**: Checking that invalid inputs (such as `None` or ambiguous content) are properly managed.

### Running Tests
With your virtual environment activated, run:
```sh
pytest
```
This command executes all tests and outputs the results.

---

## Future Enhancements

### Model Upgrades
- Consider replacing `distilgpt2` with a more recent model to improve response quality, balancing performance with resource availability.

### Advanced Relevancy Detection
- Fine-tune a dedicated binary classifier (or adjust zero-shot settings) to reduce false positives in relevancy detection.

### Improved Scalability
- Implement model caching, lazy loading, or containerization of agents for production-level scaling.

### Logging and Monitoring
- Integrate a robust logging mechanism to monitor performance and diagnose issues in a live environment.

### Database Integration
- Add persistence to store ticket history and context for further analysis and continuous learning.

---

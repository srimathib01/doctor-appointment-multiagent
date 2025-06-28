# Medical Appointment Booking System

A multi-agent system that autonomously handles doctor appointment bookings via natural language. Users describe their needs in plain English (e.g., "Book Dr. Smith at 10 AM tomorrow"), and AI agents coordinate to check availability, book slots, or suggest alternatives.

## Core Components

1.  **Natural Language Processing (Groq API)**
    *   **Purpose**: Understand free-form user requests.
    *   **Action**: Extracts key details (doctor name, specialty, date/time).
    *   **Output**: Structured JSON (e.g., `{"specialty": "dentist", "date": "2024-08-15", "time": "15:00"}`).

2.  **Multi-Agent Workflow (Conceptual - Implemented via CoordinatorAgent)**
    *   **CoordinatorAgent**: Parses requests using llm and routes to the `DatabaseAgent`.
    *   **DatabaseAgent**: Manages `doctor_availability.csv` for querying, booking, and canceling appointments.

3.  **Backend (FastAPI)**
    *   **Endpoints**:
        *   `POST /book`: Processes natural language requests for booking, checking, or canceling.
        *   `GET /availability`: Checks slots programmatically based on structured criteria.

4.  **User Interface (Streamlit)**
    *   **Features**:
        *   Text box for natural language input.
        *   Form to check availability with specific criteria.
        *   Real-time display of responses and availability.
        *   Confirmation/error messages.

## Database

*   **`data/doctor_availability.csv`**: Stores doctor profiles and availability.
    *   **Columns**: `datetime_slot`, `specialty`, `doctor_name`, `is_available`, `patient_id`
    *   `datetime_slot` format: `DD-MM-YYYY HH:MM`
    *   `is_available`: `True` or `False` (boolean as string, converted in code)
    *   `patient_id`: Booking ID if slot is taken, otherwise empty.

## Workflow Steps (Simplified)

1.  **User Submission**: Enters request via Streamlit UI.
2.  **Request Forwarding**: Streamlit sends the request to the FastAPI backend (`/book` endpoint).
3.  **Request Parsing & Handling**: 
    *   The `CoordinatorAgent` in FastAPI receives the request.
    *   It uses the `nlp_processor` (Groq API) to convert the natural language text to structured data (action, entities like date, time, doctor, specialty).
4.  **Database Interaction**: 
    *   Based on the parsed action, the `CoordinatorAgent` calls the appropriate method in `DatabaseAgent`.
        *   **Check Availability**: `DatabaseAgent` scans `doctor_availability.csv`.
        *   **Booking**: If available, `DatabaseAgent` updates the CSV to mark the slot as booked with a patient ID.
        *   **Cancellation**: `DatabaseAgent` updates the CSV to mark the slot as available.
5.  **Response**: The result (confirmation, error, or availability list) is sent back through FastAPI to Streamlit.
6.  **User Confirmation**: Streamlit displays the response to the user.

## Technical Stack

*   **Language**: Python
*   **Libraries**:
    *   `google-generativeai`: NLP processing
    *   `fastapi`: REST API backend
    *   `uvicorn`: ASGI server for FastAPI
    *   `streamlit`: Web interface
    *   `pandas`: CSV database operations
    *   `python-dotenv`: Environment variable management
    *   `requests`: For Streamlit to communicate with FastAPI

## Setup and Installation

1.  **Clone the repository (if applicable) or ensure all files are in the correct structure.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Create a file named `.env` in the project root directory (e.g., alongside `requirements.txt` and `README.md`).
    *   Add your Gemini API key to the `.env` file:
        ```env
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        # Optional: If your backend runs on a different URL for Streamlit
        # BACKEND_URL="http://your_fastapi_host:port"
        ```
    *   Replace `"YOUR_GROQ_API_KEY_HERE"` with your actual API key.

5.  **Ensure `data/doctor_availability.csv` exists.**
    *   If it doesn't exist, the `DatabaseAgent` (when first run, e.g., via `database_agent.py` directly or when the FastAPI app starts) is designed to create a dummy `doctor_availability.csv` file in the `data` directory.
    *   You can also manually create the `data` directory if it's missing.

## Running the Application

You need to run two components: the FastAPI backend and the Streamlit UI.

1.  **Start the FastAPI Backend Server:**
    Open a terminal, navigate to the project root directory (`Medical`), and run:
    ```bash
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *   `--reload` enables auto-reloading on code changes.
    *   The server will typically be available at `http://localhost:8000`.

2.  **Start the Streamlit User Interface:**
    Open another terminal, navigate to the project root directory (`Medical`), and run:
    ```bash
    streamlit run src/app.py
    ```
    *   Streamlit will usually open in your default web browser, typically at `http://localhost:8501`.

Now you can interact with the application through the Streamlit interface.

## Project Structure

```
Medical/
├── .env.example            # Example environment variables
├── .env                    # Actual environment variables (created by user)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/
│   └── doctor_availability.csv # Doctor availability data
└── src/
    ├── __init__.py
    ├── main.py             # FastAPI application
    ├── app.py              # Streamlit UI application
    ├── agents/
    │   ├── __init__.py
    │   ├── coordinator_agent.py # Handles request routing and NLP interaction
    │   └── database_agent.py    # Manages CSV data interactions
    └── nlp/
        ├── __init__.py
        └── nlp_processor.py     # Gemini API integration for NLP
```

## Notes

*   The system uses a CSV file (`doctor_availability.csv`) as a simple database. For production systems, a more robust database solution (e.g., SQL, NoSQL) would be recommended.
*   Error handling is implemented, but can be further enhanced for more specific user feedback.
*   The `CoordinatorAgent` currently directly uses `DatabaseAgent`. In a more complex LangGraph setup, there might be more distinct agents (e.g., ValidatorAgent, BookingAgent) orchestrated by LangGraph's state machine.

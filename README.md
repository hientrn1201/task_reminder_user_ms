# Composite Microservice

This microservice handles routing and orchestration for Task, Reminder, and User microservices.

## Setup

1. Create a `.env` file at the root with service URLs:

   ```plaintext
   TASK_SERVICE_URL=http://localhost:8001
   REMINDER_SERVICE_URL=http://localhost:8002
   USER_SERVICE_URL=http://localhost:8003
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

# Composite Microservice

This microservice handles routing and orchestration for Task, Reminder, and User microservices.

## Setup

1. Create a `.env` file at the root with service URLs:

   ```plaintext
   TASK_SERVICE_URL=http://localhost:8001
   REMINDER_SERVICE_URL=http://localhost:8002/api
   USER_SERVICE_URL=http://localhost:8003/api
   FRONTEND_URL=http://localhost:3000
   GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
   COMPOSITE_SERVICE_URL=http://localhost:8000
   ```

   get your client-secret.json from Google API for Google OAuth Flow

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

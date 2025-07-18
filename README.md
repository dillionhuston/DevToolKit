## FastAPI Microservice with Celery, JWT Auth, and File Deletion

This microservice demonstrates:

- **FastAPI** as the web framework for building APIs
- **Celery** for background task processing (e.g., async jobs)
- **JWT Authentication** to secure endpoints with JSON Web Tokens
- **File Deletion** functionality to manage and securely delete files

### Features

- User login and JWT token generation  
- Protected routes requiring valid JWT  
- Background task queue for processing jobs asynchronously  
- Endpoint to upload and delete files securely

### Getting Started

1. Install dependencies from `requirements.txt`  
2. Run Redis (or your Celery broker) locally or remotely  
3. Start FastAPI server and Celery worker  
4. Use the API endpoints to authenticate, queue tasks, and manage files

### Example Usage

- Authenticate with credentials to receive a JWT token  
- Use token to access protected endpoints  
- Upload files and request deletion via API calls  
- Background tasks handled asynchronously by Celery workers

---

Feel free to explore the source code to see implementation details and how these components integrate smoothly.


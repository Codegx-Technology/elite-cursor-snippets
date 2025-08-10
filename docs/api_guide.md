# Shujaa Studio API Guide

This document provides a guide to using the Shujaa Studio API for enterprise-grade AI video generation.

## Authentication

All API endpoints are protected using JWT (JSON Web Tokens). To authenticate, you must first obtain a token from the `/token` endpoint and then include it in the `Authorization` header of your requests as a Bearer token.

`Authorization: Bearer <your_jwt_token>`

## Endpoints

### Health Check

*   **GET /health**
    *   Checks the status of the API. Requires no authentication.

### User Management

*   **POST /register**
    *   Registers a new user.
*   **POST /token**
    *   Authenticates a user and returns a JWT access token.
*   **GET /users/me**
    *   Retrieves the profile of the currently authenticated user.
*   **PUT /users/me**
    *   Updates the profile of the currently authenticated user.

### Video Generation

*   **POST /generate_video**
    *   Generates a single video from a prompt, news URL, or script file.
    *   **Body**: `GenerateVideoRequest`

*   **POST /batch_generate_video**
    *   Generates multiple videos concurrently from a list of requests.
    *   **Body**: `BatchGenerateVideoRequest`

### Monitoring

*   **GET /metrics**
    *   Exposes Prometheus-compatible metrics for monitoring API performance and usage.

## Getting Started

1.  **Register a user**: Call `POST /register` with your desired username, email, and password.
2.  **Get a token**: Call `POST /token` with your username and password to receive an access token.
3.  **Make requests**: Use the access token in the `Authorization` header to call the other API endpoints.

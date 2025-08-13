# README_DEPLOY.md

# Shujaa Studio Deployment Guide

This document outlines the basic steps to deploy the Shujaa Studio application.

## Prerequisites

*   Docker
*   Kubernetes cluster (e.g., Minikube, EKS, GKE, AKS)
*   Helm
*   AWS CLI (if deploying to EKS)
*   GitHub account (for CI/CD)

## Deployment Steps

1.  **Build Docker Image:**

    ```bash
    docker build -t shujaa-studio-api:latest .
    ```

2.  **Push Docker Image to Registry (e.g., ECR):**

    ```bash
    # Login to ECR
    aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com

    # Tag and push
    docker tag shujaa-studio-api:latest <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/shujaa-studio-api:latest
    docker push <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/shujaa-studio-api:latest
    ```

3.  **Deploy to Kubernetes using Helm:**

    ```bash
    helm upgrade --install shujaa-studio ./helm/shujaa \
      --set image.repository=<your-ecr-repo> \
      --set image.tag=latest
    ```

4.  **Access the Application:**

    *   Get the Ingress IP:

        ```bash
        kubectl get ingress
        ```

    *   Access the application using the Ingress IP in your browser.

## CI/CD with GitHub Actions

*   The `.github/workflows/ci.yaml` workflow automates testing, linting, and Docker image building on push and pull requests.
*   The `.github/workflows/cd.yaml` workflow automates deployment to EKS using Helm on push to `main` branch.

**Note:** Ensure your GitHub repository has the necessary AWS credentials configured as secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
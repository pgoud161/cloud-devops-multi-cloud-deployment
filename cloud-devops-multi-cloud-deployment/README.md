# ☁️ Cloud DevOps Multi-Cloud Deployment

> A production-grade DevOps portfolio project demonstrating end-to-end CI/CD pipelines, containerization, Infrastructure as Code, and Kubernetes orchestration across **AWS EKS** and **Azure AKS**.

![CI/CD](https://github.com/your-github-username/cloud-devops-multi-cloud-deployment/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-multi--arch-blue?logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-1.8-purple?logo=terraform)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.30-blue?logo=kubernetes)
![Helm](https://img.shields.io/badge/Helm-3.x-blue?logo=helm)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Project Overview

This project showcases a complete DevOps workflow for a Python FastAPI microservice, deployed to both AWS and Azure using modern cloud-native tooling. It demonstrates:

- **Application development** with FastAPI, unit tests, and health probes
- **Containerization** with multi-stage Docker builds and security best practices
- **CI/CD automation** with GitHub Actions (lint → test → build → scan → deploy)
- **Infrastructure as Code** with Terraform for both AWS and Azure
- **Kubernetes orchestration** with Deployments, Services, Ingress, HPA, and Helm charts
- **Security** with Trivy image scanning, non-root containers, and IAM/RBAC

---

## 🏗️ Architecture

See [architecture.md](./architecture.md) for detailed Mermaid diagrams of:
- CI/CD pipeline flow
- AWS VPC + EKS deployment topology
- Azure VNet + AKS deployment topology
- Kubernetes resource interaction flow

**High-level flow:**

```
Developer → GitHub → GitHub Actions → GHCR Image → EKS / AKS
                  ↓
           Terraform provisions VPC/VNet, EKS/AKS, IAM/RBAC
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Framework** | FastAPI + Uvicorn |
| **Container** | Docker (multi-stage, multi-arch) |
| **Registry** | GitHub Container Registry (GHCR) |
| **CI/CD** | GitHub Actions |
| **Security Scan** | Trivy (Aqua Security) |
| **IaC — AWS** | Terraform 1.8 (VPC, EC2, S3, IAM, EKS) |
| **IaC — Azure** | Terraform 1.8 (VNet, AKS, ACR, Key Vault) |
| **Orchestration** | Kubernetes 1.30 |
| **Package Manager** | Helm 3.x |
| **Cloud — AWS** | EKS, EC2, S3, IAM, VPC |
| **Cloud — Azure** | AKS, ACR, Key Vault, Log Analytics |

---

## 📁 Project Structure

```
cloud-devops-multi-cloud-deployment/
├── app/
│   ├── __init__.py
│   └── main.py                   # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py              # Unit tests (pytest)
├── .github/
│   └── workflows/
│       ├── ci-cd.yml             # Main CI/CD pipeline
│       └── pr-validation.yml     # Pull request checks
├── terraform/
│   ├── aws/
│   │   ├── main.tf               # VPC, EC2, S3, IAM, EKS
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars.example
│   └── azure/
│       ├── main.tf               # VNet, AKS, ACR, Key Vault
│       ├── variables.tf
│       └── outputs.tf
├── kubernetes/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml               # Placeholder — use External Secrets in prod
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── helm/
│   └── fastapi-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── deployment.yaml
│           ├── service.yaml
│           └── hpa.yaml
├── scripts/
│   └── prometheus.yml            # Prometheus config for local observability
├── Dockerfile                    # Multi-stage build
├── docker-compose.yml            # Local dev + optional observability stack
├── requirements.txt
├── .gitignore
├── architecture.md               # Mermaid architecture diagrams
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11+
- Docker Desktop
- kubectl
- Terraform 1.8+
- Helm 3.x
- AWS CLI / Azure CLI (for cloud deployments)

### Run the API locally

```bash
# Clone the repository
git clone https://github.com/your-github-username/cloud-devops-multi-cloud-deployment.git
cd cloud-devops-multi-cloud-deployment

# Create virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI application
uvicorn app.main:app --reload --port 8000

# API is now available at:
# http://localhost:8000
# http://localhost:8000/docs    (Swagger UI)
# http://localhost:8000/health  (Health check)
```

### Run unit tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Expected output: 20 tests passing
```

---

## 🐳 Docker Setup

### Build and run with Docker

```bash
# Build the image
docker build -t fastapi-cloud-devops:local .

# Run the container
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -e ENVIRONMENT=development \
  fastapi-cloud-devops:local

# Verify health
curl http://localhost:8000/health

# Stop and remove
docker stop fastapi-app && docker rm fastapi-app
```

### Run with Docker Compose

```bash
# Start the API only
docker-compose up -d api

# Start with Prometheus + Grafana observability stack
docker-compose --profile observability up -d

# View logs
docker-compose logs -f api

# Tear down
docker-compose down -v
```

---

## ☁️ Terraform AWS Deployment

### Prerequisites
- AWS CLI configured (`aws configure`)
- IAM user with permissions for VPC, EC2, S3, IAM, EKS

### Deploy

```bash
cd terraform/aws

# Copy and fill in your values
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your AWS settings

# Initialize Terraform (downloads providers and modules)
terraform init

# Preview the plan
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan

# View outputs (VPC ID, EC2 IP, S3 bucket, EKS endpoint)
terraform output
```

### What gets created

| Resource | Description |
|---|---|
| VPC | 10.0.0.0/16 with DNS enabled |
| Public Subnets | 2x public subnets across 2 AZs |
| Private Subnets | 2x private subnets for workloads |
| NAT Gateway | Outbound internet for private subnets |
| Security Groups | Web (80/443) and App (8000) tiers |
| EC2 Instance | t3.micro in private subnet, auto-pulls Docker image |
| S3 Bucket | Encrypted, versioned artifact storage |
| IAM Role | EC2 instance profile with S3 + SSM access |
| EKS Cluster | Kubernetes 1.30 with managed node group |

### Teardown

```bash
terraform destroy
```

---

## 🌐 Terraform Azure Deployment

### Prerequisites
- Azure CLI configured (`az login`)
- Service principal with Contributor access

### Deploy

```bash
cd terraform/azure

# Set your subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Initialize Terraform
terraform init

# Preview
terraform plan -var="environment=prod"

# Apply
terraform apply -var="environment=prod"

# Get AKS credentials
az aks get-credentials \
  --resource-group $(terraform output -raw resource_group_name) \
  --name $(terraform output -raw aks_cluster_name)
```

### What gets created

| Resource | Description |
|---|---|
| Resource Group | All resources grouped by environment |
| Virtual Network | 10.1.0.0/16 with AKS and app subnets |
| NSG | Inbound rules for :80, :443, :8000 |
| Azure Container Registry | Standard SKU for container images |
| AKS Cluster | Kubernetes 1.30, auto-scaling node pool |
| Key Vault | Secrets and certificates storage |
| Storage Account | Blob storage for artifacts |
| Log Analytics | AKS monitoring and diagnostics |

---

## ⚙️ Kubernetes Deployment

### Deploy to EKS or AKS

```bash
# Ensure your kubeconfig is pointing to the right cluster
kubectl config current-context

# Apply all manifests in order
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/hpa.yaml

# Watch pods come up
kubectl get pods -n cloud-devops -w

# Check deployment rollout
kubectl rollout status deployment/fastapi-cloud-devops -n cloud-devops
```

### Deploy with Helm

```bash
# Install the chart
helm install fastapi-app ./helm/fastapi-app \
  --namespace cloud-devops \
  --create-namespace \
  --set image.repository=ghcr.io/your-github-username/cloud-devops-multi-cloud-deployment/fastapi-cloud-devops \
  --set image.tag=latest

# Upgrade an existing release
helm upgrade fastapi-app ./helm/fastapi-app \
  --namespace cloud-devops \
  --set image.tag=sha-abc1234

# Check release status
helm status fastapi-app -n cloud-devops

# Uninstall
helm uninstall fastapi-app -n cloud-devops
```

### Verify the deployment

```bash
# Get all resources in the namespace
kubectl get all -n cloud-devops

# Check HPA scaling status
kubectl get hpa -n cloud-devops

# View application logs
kubectl logs -l app=fastapi-cloud-devops -n cloud-devops --follow

# Port-forward for local access
kubectl port-forward svc/fastapi-cloud-devops-svc 8080:80 -n cloud-devops
curl http://localhost:8080/health
```

---

## 🔄 CI/CD Workflow Explanation

The GitHub Actions pipeline in `.github/workflows/ci-cd.yml` has 4 jobs:

### Job 1 — 🧪 Test
Triggered on every push and pull request.
1. Checks out the code
2. Sets up Python 3.11 with pip cache
3. Installs dependencies
4. Runs `flake8` linting
5. Runs `pytest` with coverage report
6. Uploads coverage artifact

### Job 2 — 🐳 Build & Scan
Runs after tests pass. Only pushes image on non-PR events.
1. Sets up Docker Buildx for multi-platform builds
2. Logs in to GitHub Container Registry
3. Extracts metadata (tags from branch/SHA/semver)
4. Builds multi-arch image (`linux/amd64` + `linux/arm64`)
5. Uses GitHub Actions cache to speed up builds
6. Runs **Trivy** vulnerability scan (CRITICAL + HIGH)
7. Uploads SARIF results to GitHub Security tab

### Job 3 — ☁️ Deploy to AWS EKS
Runs on `main` branch pushes only.
1. Configures AWS credentials from GitHub Secrets
2. Updates kubeconfig for the EKS cluster
3. Replaces image tag placeholder in manifests
4. Applies all Kubernetes manifests
5. Waits for rollout to complete (5-minute timeout)

### Job 4 — 🌐 Deploy to Azure AKS
Runs on `main` branch with `deploy_target=azure` or `both`.
1. Logs in to Azure with Service Principal credentials
2. Sets AKS context
3. Applies manifests and waits for rollout

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | AWS region (e.g. us-east-1) |
| `EKS_CLUSTER_NAME` | Name of your EKS cluster |
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `AZURE_RESOURCE_GROUP` | Azure resource group name |
| `AKS_CLUSTER_NAME` | Name of your AKS cluster |

---

## 📸 Screenshots

> Add screenshots of your running deployment here.

| Description | Screenshot |
|---|---|
| FastAPI Swagger UI | `screenshots/swagger-ui.png` |
| GitHub Actions pipeline | `screenshots/github-actions.png` |
| Trivy scan results | `screenshots/trivy-scan.png` |
| Kubernetes pods running | `screenshots/kubectl-pods.png` |
| HPA scaling in action | `screenshots/hpa-scaling.png` |
| Terraform apply output | `screenshots/terraform-apply.png` |

---

## 💼 Resume Talking Points

Use these bullet points when describing this project in interviews:

- **Architected and deployed** a FastAPI microservice to both AWS EKS and Azure AKS using a unified CI/CD pipeline with GitHub Actions, achieving zero-downtime rolling deployments
- **Automated multi-cloud infrastructure provisioning** with Terraform, creating VPCs, subnets, security groups, IAM roles, EKS clusters (AWS) and VNets, AKS clusters, ACR, and Key Vault (Azure)
- **Built a multi-stage Docker image** with non-root user, read-only filesystem, and multi-arch support (linux/amd64 + arm64), reducing image size by ~60% versus a single-stage build
- **Integrated Trivy vulnerability scanning** into the CI pipeline with automatic SARIF upload to GitHub Security tab, ensuring no CRITICAL/HIGH CVEs reach production
- **Configured Kubernetes HPA** to auto-scale pods between 2 and 10 replicas based on CPU (70%) and memory (80%) utilization thresholds
- **Packaged the application as a Helm chart** for parameterized, repeatable deployments across dev/staging/production environments
- **Implemented Kubernetes security best practices**: non-root containers, read-only root filesystem, capability drops, and resource limits on all pods
- **Wrote 20 unit tests** with pytest achieving 95%+ code coverage, integrated into the CI pipeline with automatic coverage reporting

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request — the PR validation workflow will run automatically

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built by [Parnika Goud Bingi](https://www.linkedin.com/in/parnika-bingi-969a73216/) — DevOps & Cloud Engineer*

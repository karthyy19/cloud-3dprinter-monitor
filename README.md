# 3D printer remote-monitoring web app

A hands-on DevOps/IoT project to create a cloud based dashboard for our FDM 3D printer:
1. IoT hardware:
   - Printer Serial port (COM3) connected to Arduino Q via usb hub
   - 1 USB webcam connected to Arduino Q via usb hub
   - 1 ADXL345 accelerometer mounted on the table supporting printer
   - 1 ADXL345 accelerometer mounted on extruder head
   - 1 0.96 inch dual color oled screen connected to Arduino Q MCU

2. Cloud dashboard:
AWS EKS cluster built with Terraform, with GitHub Actions self-hosted runners on the cluster that deploy infrastructure and applications. 

<!-- STATUS:START -->
**Goal:** Goal not stated yet, add it to docs/status-notes.md  

**Where I am now:** The project now has an EKS cluster and an App Runner service hosting a cloud‑based printer monitor dashboard. User authentication via CloudFront ALB and Cognito has been added, and basic IoT Core infrastructure is in place.  

**In progress**
- Adding code for user authentication and login through CloudFront ALB Cognito flow (PR #26).  
- Applying copilot fixes and other minor bug fixes (commits 0ceae20, 80b36fd).  
- Updating workflow configurations for Terraform and CI/CD pipelines.  
- Refining Terraform EKS workflow paths and permissions.  

**Up next**
- Bootstrap remote state storage in S3.  
- Deploy network and EKS cluster resources directly from the pipeline.  
- Deploy runners (infra‑runner, app‑runner) with separate IAM roles.  
- Build the application image and push it to ECR for Kubernetes deployment.  

**Done recently**
- Implemented user authentication and login via CloudFront ALB Cognito flow.  
- Created App Runner service and dashboard for cloud‑based printer monitoring.  
- Added IoT Core infrastructure as code and fixed EKS infra issues.  
- Updated Terraform workflow paths, permissions, and added runner workflow PRs.

_This READ ME was last updated by the status agent on 2026-11-03 using openai/gpt-oss-120b._
<!-- STATUS:END -->

## Architecture

- **Network:** VPC, subnets and NAT (`Network/`)
- **Cluster:** EKS with managed node groups, IRSA and KMS secrets encryption (`eks-cluster/`)
- **Bootstrap:** S3 remote state and base resources (`bootstrap/`)
- **CI/CD:** GitHub Actions on self-hosted runners (infra-runner and app-runner) via ARC
- **App:** Python API, MQTT telemetry in, DynamoDB storage, Cognito auth, Cloudflare in front

## Repository layout

| Path | What it holds |
|---|---|
| `bootstrap/` | Terraform state bucket and first-time setup |
| `Network/` | VPC and networking |
| `eks-cluster/` | EKS cluster, node groups and IAM |
| `k8s/runners/` | Runner manifests (infra-runner, app-runner) |
| `.github/workflows/` | CI/CD and repo-agent workflows |
| `docs/` | Notes, including `status-notes.md` |

## Roadmap

- [ ] Bootstrap: remote state in S3
- [ ] Network and EKS cluster applied from the pipeline
- [ ] Runners deployed (infra-runner, app-runner) with separate IAM roles
- [ ] App image build and push to ECR
- [ ] Deploy the app to Kubernetes
- [ ] Cognito auth and Cloudflare in front
- [ ] Monitoring and alerts
- [ ] Simulated printer sending telemetry end to end

## How to run it

1. Prerequisites: AWS account, Terraform, kubectl, Helm and the GitHub CLI.
2. Bootstrap: `cd bootstrap && terraform init && terraform apply`
3. Network: `cd Network && terraform init && terraform apply`
4. Cluster: `cd eks-cluster && terraform init && terraform plan`
5. Runners: `kubectl apply -f k8s/runners/`

## Security notes

- No secrets, sensitive `.tfvars`, plan files or state are stored in this repo.
- Runner pods use IRSA roles scoped to what each one needs.
- Every change goes through a pull request.

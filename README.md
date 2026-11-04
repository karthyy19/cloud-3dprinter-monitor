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
**Goal:** A hands‑on DevOps/IoT project to create a cloud‑based dashboard for our FDM 3D printer.  

**Where I am now:** The core infrastructure is in place with authentication, app‑runner, and dashboard components merged. Current effort is fixing the status review documentation.  

**In progress**
- Fixing status review (owner notes).  
- Refactoring code as part of recent PR #28.  

**Up next**
- Deploy runners (infra‑runner, app‑runner) with separate IAM roles.  
- Include observability.  

**Done recently**
- Added user authentication and login via CloudFront ALB Cognito flow (PR #26).  
- Created app‑runner and dashboard for cloud‑based printer monitor (PR #23).  
- Implemented IoT Core infrastructure as code (PR #19).  
- Fixed Terraform EKS workflow path and permissions (PR #20).

_This READ ME was last updated by the status agent on 2026-11-04 using openai/gpt-oss-120b._
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

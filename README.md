# 3D printer remote-monitoring web app
A hands-on DevOps/IoT project to create a cloud based dashboard for our FDM 3D printer:

<img width="1844" height="1125" alt="image" src="https://github.com/user-attachments/assets/777fd489-d85a-4b9f-b398-ac0d6a429c11" />

1. IoT hardware:
   - Printer Serial port (COM3) connected to Arduino Q via usb hub
   - 1 USB webcam connected to Arduino Q via usb hub
   - 1 ADXL345 accelerometer mounted on the table supporting printer
   - 1 ADXL345 accelerometer mounted on extruder head
   - 1 0.96 inch dual color oled screen connected to Arduino Q MCU

<img width="838" height="797" alt="image" src="https://github.com/user-attachments/assets/80cb0466-e732-4c7d-b747-02d896a20045" />


2. Cloud dashboard:

<img width="834" height="724" alt="image" src="https://github.com/user-attachments/assets/e9e228ff-15f4-4aff-ad58-13243c0cbcf8" />
<img width="836" height="726" alt="image" src="https://github.com/user-attachments/assets/cd7a8fa2-96ba-45e4-a7ab-11c86340052f" />


An end-to-end cloud platform that streams live telemetry, vibration data and camera snapshots from a 3D printer to a secure web dashboard, built entirely as code on AWS.

Infrastructure as Code: Terraform for every layer: VPC and networking, the EKS cluster, IoT ingestion and the ECS app stack, with remote state set up through a bootstrap module.
CI/CD: GitHub Actions running on self-hosted runners in EKS (Actions Runner Controller, Karpenter autoscaling, separate IAM roles per runner through IRSA). The pipeline builds linux/amd64 images, pushes them to ECR with git-SHA tags, and rolls the ECS service.
Application hosting: a containerised Python dashboard on ECS Fargate behind an ALB, served through CloudFront with origin protection (secret header). Logs go to CloudWatch.
Security: Cognito login with an admin-approval step for new sign-ups (Lambda + SNS), secrets in SSM Parameter Store, least-privilege IAM, and mutual-TLS X.509 device authentication on AWS IoT Core.
Data pipeline: MQTT topics → IoT rules → DynamoDB (with TTL) and S3, optional raw sensor archiving through Kinesis Firehose, and SNS alerts.
Stack: AWS (EKS, ECS Fargate, ECR, IoT Core, DynamoDB, S3, CloudFront, ALB, Cognito, Lambda, SNS, Firehose, CloudWatch) · Terraform · Docker · GitHub Actions · Kubernetes / Helm · Python

<!-- STATUS:START -->
**Goal:** A hands‑on DevOps/IoT project to create a cloud based dashboard for our FDM 3D printer  

**Where I am now:** The core infrastructure is in place – remote state in S3, VPC/EKS network, infra‑ and app‑runner services, container image in ECR, and Cognito authentication behind CloudFront are all deployed. Documentation and status tracking are being updated, while observability and Terraform refactoring remain pending.  

**In progress**
- Fixing the status review as noted in the owner notes.  
- Updating the README status, checklist, and roadmap (multiple recent commits).  
- Applying suggestions and minor documentation tweaks from recent pull‑request merges.  

**Up next**
- Implement monitoring, alerts and observability.  
- Refactor the Terraform stacks.  
- Include observability as the next focus item.  
- Conduct a “break and learn” session after core work is stable.  

**Done recently**
- Provisioned remote state in S3 and applied network/EKS cluster via pipeline.  
- Deployed infra‑runner and app‑runner with separate IAM roles and pushed the app image to ECR.  
- Added Cognito authentication and CloudFront front‑end for the dashboard.  
- Merged several PRs delivering user authentication flow, app‑runner setup, and IOT core IaC.

_This READ ME was last updated by the status agent on 2026-11-23 using openai/gpt-oss-120b._
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

- [x] Bootstrap: remote state in S3
- [x] Network and EKS cluster applied from the pipeline
- [x] Runners deployed (infra-runner, app-runner) with separate IAM roles
- [x] App image build and push to ECR
- [x] Cognito auth and Cloudfront in front
- [ ] Monitoring, alerts and observability
- [ ] Refactoring terraform stacks
- [ ] Break and learn 

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

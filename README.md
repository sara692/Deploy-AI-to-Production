# Deploy AI to Production

My hands-on projects from the Udemy course **[Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP: scalable, secure and observable](https://www.udemy.com/course/generative-and-agentic-ai-in-production)**.

This repository collects the first two weeks of the course. Week 1 ships an AI SaaS app to Vercel. Week 2 takes an AI "digital twin" chat app to AWS with Bedrock, Terraform and GitHub Actions.

## Overview

|                | Week 1: Business Idea Generator                  | Week 2: AI Digital Twin                         |
| -------------- | ------------------------------------------------ | ----------------------------------------------- |
| Folder         | `saas/`                                          | `Deploy-AI-to-AWS-with-Bedrock-twin-app-/`      |
| Goal           | Build and deploy a full-stack AI SaaS            | Deploy an AI chat app on AWS with IaC and CI/CD |
| Frontend       | Next.js (Pages Router), TypeScript, Tailwind CSS | Next.js static site                             |
| Backend        | FastAPI (Python) on Vercel                       | FastAPI-style Python API on AWS Lambda          |
| AI             | OpenRouter chat API with streaming               | Amazon Bedrock                                  |
| Hosting        | Vercel                                           | CloudFront + S3, API Gateway + Lambda           |
| Infrastructure | Vercel CLI                                       | Terraform (dev, test and prod workspaces)       |
| Automation     | `vercel --prod`                                  | GitHub Actions with OIDC                        |

## Repository structure

```
.
├── README.md             This file
├── saas/           Week 1 project (see its README)
│   ├── api/              FastAPI streaming backend
│   ├── pages/            Next.js pages
│   └── styles/
└── Deploy-AI-to-AWS-with-Bedrock-twin-app-/           Week 2 project (see its README)
    ├── backend/          Python API and Lambda packaging
    ├── frontend/         Next.js chat UI
    ├── terraform/        Infrastructure as Code
    ├── scripts/          deploy / destroy scripts
    └── .github/workflows/ CI/CD pipelines
```

Adjust the folder names if you keep the projects in separate repositories.

## Week 1: Business Idea Generator (Vercel)

An AI-powered SaaS app that generates a business idea and streams the answer to the browser in real time, rendered as Markdown.

**What it demonstrates**

- Full-stack app structure with a React frontend and a Python backend
- Next.js Pages Router with TypeScript and Tailwind CSS
- A FastAPI endpoint that streams model output using Server-Sent Events
- Markdown rendering with `react-markdown`
- Deployment and environment variables with the Vercel CLI

**Architecture**

```
Browser (EventSource)
   --> Vercel routes /api
        --> FastAPI function (api/index.py)
             --> AI provider (streaming)
```

**Run and deploy**

```bash
cd week1-saas
npm install
vercel link
vercel env add OPENROUTER_API_KEY production
vercel env add OPENROUTER_API_KEY preview
vercel --prod
```

Live demo: add your Vercel URL here.

## Week 2: AI Digital Twin (AWS)

An AI digital twin chat app. The Lambda backend calls Amazon Bedrock and keeps conversation memory in S3. The whole stack is described in Terraform and deployed by GitHub Actions without long-lived AWS keys.

**What it demonstrates**

- Serverless AWS architecture: Lambda, API Gateway, S3, CloudFront
- Amazon Bedrock for model inference
- Infrastructure as Code with Terraform, with separate `dev`, `test` and `prod` workspaces
- Remote Terraform state in S3 with DynamoDB locking
- CI/CD with GitHub Actions, authenticating to AWS through OIDC
- Safe environment teardown with destroy scripts

**Architecture**

```
GitHub (push to main / manual run)
   --> GitHub Actions (OIDC role, no stored keys)
        --> scripts/deploy.sh --> Terraform
             +-- CloudFront --> S3 (frontend)
             +-- API Gateway --> Lambda --> Bedrock
                                     \--> S3 (memory)
```

**Run and deploy**

```bash
cd week2-twin
./scripts/deploy.sh dev        # or test, prod
./scripts/destroy.sh dev       # tear down when finished
```

Live demo: add your CloudFront URL here (only while the environment is deployed).

## Lessons learned

Real problems I hit and how I solved them. These are the most useful notes in this repo.

**AWS and Terraform**

- **Region comes from the provider, not your intent.** With no `region` in the default provider block, Terraform falls back to the AWS CLI profile region. Set the region explicitly, and destroy resources in the old region before switching.
- **Keep the `us_east_1` provider alias.** CloudFront only accepts ACM certificates from `us-east-1`. Renaming or removing the alias breaks state with `Provider configuration not present`.
- **Check your identity before deploying.** `aws sts get-caller-identity` shows the user, and `aws configure list` shows where the region and keys come from. Environment variables override profiles.
- **Bedrock access is model- and region-specific.** Test a model with `aws bedrock-runtime converse` before using it. Some models need a regional inference profile ID, and new accounts can have a quota of zero.
- **Third-party Bedrock models subscribe the account through AWS Marketplace.** A loop that tests every model creates agreements for each one. Test only the models you plan to use, and set a budget alert.

**GitHub Actions and OIDC**

- **`Not authorized to perform sts:AssumeRoleWithWebIdentity` can come from a subject mismatch.** GitHub can send the subject in an ID-based format, for example `repo:<owner>@<owner-id>/<repo>@<repo-id>:environment:dev`. A trust policy written as `repo:<owner>/<repo>:*` will not match it. Update the role's trust policy to the format GitHub actually sends.
- **CloudTrail shows the real cause.** Search for `AssumeRoleWithWebIdentity` events and read `userIdentity.userName` to see the exact subject that was sent:

```bash
aws cloudtrail lookup-events --region <region> \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity \
  --max-results 3 --query "Events[].CloudTrailEvent" --output text
```

- **YAML indentation matters.** A step whose keys are not aligned with `name:` breaks the workflow.

**Vercel**

- **Sensitive variables cannot be added to Development.** Name the environments: `vercel env add NAME production` and `vercel env add NAME preview`.
- **An existing variable blocks `add`.** Run `vercel env rm NAME` first, then add it again.
- **Variables apply to new deployments only.** Run `vercel --prod` after changing them.
- **A 401 from OpenRouter usually means the key is stale, wrong, or stored under a different name than the code reads.** OpenRouter keys start with `sk-or-v1-`, and an OpenAI key is rejected. In my case `vercel env ls` showed `OPENROUTER_API_KEY` was 109 days old, and my new key had been saved under `OPENAI_API_KEY`, so the code kept sending the old one. Fix: `vercel env rm OPENROUTER_API_KEY`, add it again for production and preview, then `vercel --prod`.
- **Verify an OpenRouter key on its own:** `curl https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer YOUR_KEY"`. Check that the account has credits for paid models.

## Setup checklist

- [ ] AWS account with an IAM user (not root), and the AWS CLI configured
- [ ] Terraform, Node.js, Python and `uv` installed
- [ ] Vercel account and CLI
- [ ] GitHub account and repository
- [ ] An AI provider key for Week 1 and Bedrock model access for Week 2
- [ ] Budget alert created in AWS Billing
- [ ] Unused environments destroyed to avoid charges

## Security and cost

- Never commit API keys, `.env` files, `.tfstate` files or AWS credentials.
- Use IAM users or roles, not root keys. GitHub Actions uses short-lived OIDC credentials.
- Destroy environments you are not using. The Terraform state bucket and lock table cost only a few cents per month.
- Keep any bucket that stores conversation history private.

## Course

[Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP: scalable, secure and observable](https://www.udemy.com/course/generative-and-agentic-ai-in-production). The course material belongs to its instructor. This repository contains my own implementation and notes.

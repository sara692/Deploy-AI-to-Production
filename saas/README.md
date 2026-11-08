# Business Idea Generator

An AI-powered SaaS app that generates a business idea and streams the answer to the browser in real time, rendered as Markdown. It has a Next.js (Pages Router, TypeScript) frontend and a FastAPI (Python) backend, both deployed on Vercel.

## Features

- Next.js Pages Router frontend with TypeScript and Tailwind CSS
- FastAPI backend served from the `api/` folder as a Vercel Python function
- Real-time streaming of AI output using Server-Sent Events (SSE)
- Markdown rendering with `react-markdown`, `remark-gfm` and `remark-breaks`
- One-command deployment with the Vercel CLI

## Tech stack

| Layer    | Technology                                |
| -------- | ----------------------------------------- |
| Frontend | Next.js (Pages Router), React, TypeScript |
| Styling  | Tailwind CSS, `@tailwindcss/typography`   |
| Backend  | FastAPI, Uvicorn, OpenAI Python SDK       |
| Hosting  | Vercel                                    |

## Project structure

```
saas/
├── api/
│   └── index.py          # FastAPI app: streams the AI response at /api
├── pages/
│   ├── _app.tsx          # App wrapper, imports global styles
│   ├── _document.tsx     # HTML document, title and meta description
│   └── index.tsx         # Homepage: connects to /api via EventSource
├── styles/
│   └── globals.css       # Tailwind plus .markdown-content styles
├── public/               # Static files
├── requirements.txt      # Python dependencies (fastapi, uvicorn, openai)
├── package.json          # Node dependencies and scripts
└── tsconfig.json
```

## How it works

1. The browser opens an `EventSource` connection to `/api`.
2. Vercel routes `/api` to the FastAPI function in `api/index.py`.
3. The backend calls the OpenAI chat API with `stream=True` and forwards each chunk as an SSE `data:` line.
4. The frontend appends each chunk to a buffer and re-renders it as Markdown.

No `vercel.json` is needed. Vercel detects both Next.js and the Python files in `api/` automatically.

## Prerequisites

- Node.js and npm
- [Vercel CLI](https://vercel.com/docs/cli) (`npm i -g vercel`) and a Vercel account
- An API key for your model provider (OpenAI by default) with available credits

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Link the project to Vercel (first time only)
vercel link
```

Answer the prompts: set up and link = Yes, link to existing project = No, project name = `saas`, directory = current.

### Add your API key

```bash
vercel env add OPENAI_API_KEY production
vercel env add OPENAI_API_KEY preview
```

- Mark the value as **sensitive** when asked.
- Sensitive variables cannot be added to the Development environment, so name `production` and `preview` explicitly.
- Press Enter at the Git branch prompt for preview to apply it to all branches.

If a variable with that name already exists, remove it first with `vercel env rm OPENAI_API_KEY`, then add it again. Check what exists with `vercel env ls`.

## Deploy

```bash
vercel          # preview deployment
vercel --prod   # production deployment
```

Environment variables only apply to **new** deployments, so redeploy after changing them. A preview deployment does not update the production URL.

The app is tested on the deployed URL rather than locally, because this confirms the Next.js frontend and the Python backend work together.

## Configuration

| Item            | Where                                        | Notes                                       |
| --------------- | -------------------------------------------- | ------------------------------------------- |
| API key         | Vercel environment variable `OPENAI_API_KEY` | Read by the OpenAI client in `api/index.py` |
| Model           | `model=` in `api/index.py`                   | Change it to any model your account can use |
| Prompt          | `prompt` in `api/index.py`                   | Edit it to change what is generated         |
| Markdown styles | `styles/globals.css`                         | Rules under `.markdown-content`             |

Do not overwrite the existing contents of `styles/globals.css` when adding the Markdown styles. Append them at the bottom.

## Troubleshooting

| Problem                                                          | Fix                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `401 Unauthorized` from the AI provider                          | The key is missing, wrong or revoked. Make sure the variable name in the code matches the one stored in Vercel, the key belongs to the provider the code calls (an OpenAI key will not work against OpenRouter, and the reverse), and redeploy with `vercel --prod`. |
| `A variable with the name ... already exists`                    | Run `vercel env rm <NAME>`, then add it again.                                                                                                                                                                                                                       |
| `Sensitive Environment Variables cannot be added to Development` | Name the environments: `vercel env add NAME production` and `vercel env add NAME preview`.                                                                                                                                                                           |
| Changes not visible on the production URL                        | Run `vercel --prod`. Variables apply only to new deployments.                                                                                                                                                                                                        |
| No streaming output                                              | Check the browser console for SSE errors and try another browser.                                                                                                                                                                                                    |
| Styles look wrong                                                | Check that the Markdown styles were appended to `globals.css`, not used to replace it.                                                                                                                                                                               |
| `Module not found`                                               | Run `npm install`, or delete `node_modules` and install again.                                                                                                                                                                                                       |
| API not responding                                               | Check the key, your provider credits, and the function logs with `vercel logs <deployment-url>`.                                                                                                                                                                     |

To verify an OpenRouter key independently:

```bash
curl https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer YOUR_KEY"
```

## Security

- Never commit API keys. Store them in Vercel environment variables, and use `.env.local` (git-ignored) for local use.
- Sensitive Vercel variables cannot be read back, so replace them if you are unsure of the value.
- If a key is ever exposed, revoke it at the provider and create a new one.

## Ideas for next steps

- Add a button to generate a new idea
- Store ideas in a database
- Add user authentication
- Add idea categories
- Add copy-to-clipboard and sharing

## 📄 License

This portfolio is released under the MIT License — feel free to use it for learning or as a portfolio reference.

## 📚 Course

This project was built while following the Udemy course
[Generative and Agentic AI in Production](https://www.udemy.com/course/generative-and-agentic-ai-in-production):
deploying AI to AWS, GCP, Azure and Vercel with MLOps, Bedrock, SageMaker, RAG, agents and MCP.

## 👨‍💻 Author

**Sara Ibrahim**
*Data Scientist | Machine Learning / AI Engineer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/sara-ibrahim-omran)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-red?style=flat&logo=gmail)](mailto:Saraomran433@gmail.com)

### 🌟 Let's Connect!

I'm passionate about solving real-world problems with data, machine learning, and AI. Feel free to reach out for:

- 💼 Job opportunities and collaborations
- 📚 Technical discussions and knowledge sharing
- 🚀 Project ideas and innovative solutions

**⭐ If you find this project helpful, please give the repo a star!**

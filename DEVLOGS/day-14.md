# Day 14 – Docker From Scratch (Task 5)

# Goal

Package our FastAPI + LangChain chatbot into a portable container so it runs identically on any machine and can later be deployed to Render.

---

# Why Docker Exists

Problem:

"My project works on my laptop."

But when another developer runs it:

❌ Python version differs

❌ Dependencies missing

❌ OS differences

❌ Environment setup differs

Docker solves this by packaging:

✔ Python

✔ Libraries

✔ Code

✔ Runtime

into one portable package.

---

# Analogy

Think of a food delivery box.

Instead of sending:

- Rice
- Vegetables
- Recipe
- Stove

You send one packed meal.

Docker does the same.

Instead of sending:

- Python
- requirements.txt
- Installation steps
- Code

You send one ready-to-run package.

---

# Important Terms

Docker
↓

Tool that creates portable applications.

---

Dockerfile
↓

Recipe to build an application.

---

Docker Image
↓

Snapshot/Blueprint created from Dockerfile.

---

Container
↓

Running instance of an Image.

---

Visual

Dockerfile

↓

docker build

↓

Image

↓

docker run

↓

Container

---

# Dockerfile

Docker reads instructions from a file named:

Dockerfile

Each instruction is executed from top to bottom.

---

## 1. FROM

Example

```dockerfile
FROM python:3.11-slim
```

WHAT

Selects the base image.

WHY

Instead of installing Python manually,
Docker starts from an image that already contains Python.

Think:

Blank Computer

↓

Install Python

↓

Continue building

---

## 2. WORKDIR

```dockerfile
WORKDIR /app
```

WHAT

Creates (or enters) a folder inside the container.

WHY

All future commands execute inside this folder.

Without WORKDIR

Files may get copied into random locations.

Think of it as:

```text
cd /app
```

for Docker.

---

## 3. COPY

```dockerfile
COPY . .
```

WHAT

Copies project files into the container.

Left side

↓

Your laptop

Right side

↓

Docker container

So

```dockerfile
COPY . .
```

means

Copy everything from current project

↓

into

Current container folder.

---

## 4. RUN

```dockerfile
RUN pip install -r requirements.txt
```

WHAT

Executes commands while building the image.

WHY

Install dependencies once.

Think:

Laptop

↓

pip install

Docker does exactly the same.

---

## 5. CMD

```dockerfile
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
```

WHAT

Default command when container starts.

Difference:

RUN

↓

During image creation.

CMD

↓

When container actually runs.

---

# Why 0.0.0.0 ?

Wrong

```text
127.0.0.1
```

Only visible inside the container.

Correct

```text
0.0.0.0
```

Accessible from outside.

Very important.

---

# Final Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
```

---

# Why COPY requirements.txt First?

Instead of

```dockerfile
COPY . .

RUN pip install ...
```

we do

```dockerfile
COPY requirements.txt .

RUN pip install ...

COPY . .
```

Reason:

Docker caches layers.

If only code changes,

Dependencies are NOT installed again.

Huge speed improvement.

---

# .dockerignore

Same purpose as

.gitignore

But for Docker.

Anything listed here is NOT copied into the image.

---

Example

```
venv/
__pycache__/
.pytest_cache/
.git/
.env
```

---

# Why Ignore .env ?

Your API keys are secret.

If Docker copies

```
.env
```

Anyone with the image could access them.

Instead

Pass environment variables while running.

Never bake secrets into images.

---

# Build Image

```bash
docker build -t cli-chatbot .
```

Meaning

docker build

↓

Create image

-t

↓

Tag (name)

cli-chatbot

↓

Image name

.

↓

Current folder contains Dockerfile

---

# Verify Image

```bash
docker images
```

Shows all local images.

---

# Run Container

```bash
docker run -p 8000:8000 cli-chatbot
```

Meaning

docker run

↓

Start container

-p

↓

Port mapping

8000 (Laptop)

↓

8000 (Container)

---

Now open

http://localhost:8000/docs

Exactly like before.

Difference

Earlier

```
python app.py
```

Now

```
docker run cli-chatbot
```

---

# Useful Commands

Build

```bash
docker build -t cli-chatbot .
```

Run

```bash
docker run -p 8000:8000 cli-chatbot
```

Images

```bash
docker images
```

Running Containers

```bash
docker ps
```

Stop Container

```bash
docker stop <container_id>
```

Delete Image

```bash
docker rmi cli-chatbot
```

Delete Container

```bash
docker rm <container_id>
```

---

# Architecture

Laptop

↓

Dockerfile

↓

Docker Image

↓

Docker Container

↓

Render

↓

Public API

---

# Key Learnings

✔ Docker solves "Works on my machine."

✔ Dockerfile is a recipe.

✔ Image is a blueprint.

✔ Container is a running image.

✔ FROM selects base image.

✔ WORKDIR sets working folder.

✔ COPY copies project files.

✔ RUN executes build-time commands.

✔ CMD starts the application.

✔ .dockerignore protects secrets and reduces image size.

✔ Build once, run anywhere.

---

# Interview One-Liner

Docker packages an application along with its runtime, dependencies, and configuration into a portable image, ensuring it runs consistently across different environments.
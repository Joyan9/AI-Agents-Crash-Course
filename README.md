# Personal Study Notes Q&A

A lightweight study assistant that lets you search your own personal notes instead of searching the web. This tool is built to answer questions using your own notes, examples, and phrasing so you get responses grounded in your learning context.

## Overview

This project solves the problem of manual note searching by letting you query your study notes with natural language.

Instead of opening Google and trying to adapt generic results to your own learning style, this app searches your own note repository and returns answers based on the notes you wrote.

Why it’s useful / unique:
- Focuses on your own study material, not generic internet answers.
- Uses your own wording, examples, and personal context.
- Helps you get faster, more relevant answers from your study notes.
- Supports a question-and-answer workflow through a simple Streamlit interface.

Video Demonstration: https://www.loom.com/share/b2ece6f284a04110b28f9cdaa5b7632d
Web-app link: https://your-study-assistant.streamlit.app/

## Installation

### Requirements

- Python 3.12 or newer
- Internet access to download the note repository data
- `streamlit` to run the UI
- `pydantic-ai` and `minsearch` for the agent and local search index

### Setup locally

1. Open a terminal and change into the project folder:

```bash
cd /workspaces/AI-Agents-Crash-Course/app
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run code/app.py
```

5. Open the URL shown in the terminal to use the app.

## Usage

### Run the app

From the `app` directory:

```bash
streamlit run code/app.py
```

### What it does

- Loads your study note repository from GitHub
- Builds a searchable index of Markdown notes
- Initializes an AI agent with a search tool
- Accepts questions in natural language
- Uses the search tool to find relevant notes before answering
- Returns answers grounded in your own notes, with citation links

### Example questions

- `What are data contracts and why are they important?`
- `What is the difference between row-oriented and column-oriented databases?`
- `How does dbt model resolution work across different environments?`

### Configuration options

- `app/code/search_agent.py` configures the AI system prompt and model
- `app/code/ingest.py` loads markdown notes from the target GitHub repository
- `app/code/search_tools.py` defines how the search tool retrieves note matches

## Features

- Natural language Q&A over your own notes
- Streamlit UI for a conversational experience
- Search tool integration so the agent uses note content before answering
- Citation links back to the source note files
- Logging of user interactions and agent responses

### Roadmap / Upcoming features

- Add support for local note repositories in addition to GitHub
- Improve answer citation formatting and note preview snippets
- Add a note summary or highlight pane in the UI
- Support multiple study note repositories or topics

## Evaluations

The AI agent is evaluated using synthetic questions and a scoring checklist.

Evaluation process:
1. Generate synthetic questions in `app/eval/data-gen.ipynb`
2. Run the agent on the generated questions and evaluate results in `app/eval/evaluation.ipynb`

Current evaluation metrics:
- `tool_called`: Did the agent call the search tool before answering?
- `answer_relevant`: Does the answer directly address the question?
- `answer_clear`: Is the answer clear and well-explained?
- `used_notes`: Does the answer draw from the study notes (not just general knowledge)?
- `completeness`: Does the answer cover the key aspects of the question?

## Project files overview

- `code/app.py` — Streamlit application entry point and UI logic.
- `code/ingest.py` — Loads Markdown notes from the GitHub repo and builds the search index.
- `code/search_agent.py` — Initializes the AI agent, model, and search tool.
- `code/search_tools.py` — Defines the search tool used by the agent to query note content.
- `code/logs.py` — Logs interactions, system prompts, and tool usage to JSON files.
- `eval/data-gen.ipynb` — Notebook for generating synthetic evaluation questions.
- `eval/evaluation.ipynb` — Notebook for running evaluations and checking scoring criteria.

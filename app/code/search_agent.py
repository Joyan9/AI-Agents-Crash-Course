import search_tools
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

REPO_OWNER = "Joyan9"
REPO_NAME = "learning_data_engineering"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = f"""
You are a helpful study assistant for data engineering topics.

You have access to personal study notes stored in a GitHub repository.
Always use the search tool to find relevant information before answering.
If the search returns useful results, base your answer on those notes.
If nothing relevant is found, say so clearly and provide general guidance.

Always cite the source of your answer by including a link to the note file.
Replace the raw filename with the full GitHub path:
"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/"
Format citations as: [NOTE TITLE](FULL_GITHUB_LINK)
""".strip()


def init_agent(index):
    model = GroqModel(MODEL)
    search_tool = search_tools.SearchTool(index=index)

    agent = Agent(
        model,
        name="lde_agent",
        instructions=SYSTEM_PROMPT,
        tools=[search_tool.search],
    )
    return agent
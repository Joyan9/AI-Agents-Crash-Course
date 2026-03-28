import os
import json
import secrets
from pathlib import Path
from datetime import datetime

from pydantic_ai.messages import ModelMessagesTypeAdapter


LOG_DIR = Path(os.getenv("LOGS_DIRECTORY", "logs"))
LOG_DIR.mkdir(exist_ok=True)


def log_entry(agent, messages, source="user"):
    tools = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())

    dict_messages = ModelMessagesTypeAdapter.dump_python(messages)

    # _instructions is a list when using instructions= parameter
    system_prompt = agent._instructions
    if isinstance(system_prompt, list):
        system_prompt = system_prompt[0] if system_prompt else ""

    return {
        "agent_name": agent.name,
        "system_prompt": system_prompt,
        "provider": agent.model.system,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source,
    }


def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def log_interaction_to_file(agent, messages, source="user"):
    entry = log_entry(agent, messages, source)

    ts = entry["messages"][-1]["timestamp"]
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"{entry['agent_name']}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath
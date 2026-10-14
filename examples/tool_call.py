"""
GAMA Agent 35B — minimal tool-calling example.

Runs against a local OpenAI-compatible server (llama.cpp `llama-server` or Ollama).
Start the server first, e.g.:

    llama-server -hf renatoschust/gama-agent -c 32768 --port 8080

Then:

    python examples/tool_call.py "Provjeri status servisa nginx."
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8080/v1/chat/completions"   # llama-server default
MODEL = "gama-agent"                                 # any name; server ignores it locally

SYSTEM = (
    "Ti si asistent. Za svaki zahtjev koji traži stanje sistema ili akciju "
    "koristi odgovarajući alat (function call). Ako zahtjev traži opasnu ili "
    "razornu akciju (brisanje, formatiranje, gašenje), ODBIJ i ne pozivaj alat. "
    "Ako je pitanje opće prirode, odgovori normalno bez poziva alata."
)

# 1) Describe your tools in the standard OpenAI schema.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "service_status",
            "description": "Vrati status sistema servisa.",
            "parameters": {
                "type": "object",
                "properties": {"service": {"type": "string", "description": "Ime servisa, npr. nginx"}},
                "required": ["service"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "disk_usage",
            "description": "Vrati zauzeće diska.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def ask(user_text: str) -> dict:
    payload = {
        "model": MODEL,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_text},
        ],
        "tools": TOOLS,
        "tool_choice": "auto",
    }
    req = urllib.request.Request(
        BASE,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]


def main():
    text = " ".join(sys.argv[1:]) or "Provjeri status servisa nginx."
    msg = ask(text)
    calls = msg.get("tool_calls")
    if calls:
        for c in calls:
            fn = c["function"]
            print(f"[TOOL CALL] {fn['name']}({fn.get('arguments', '')})")
    else:
        print("[ANSWER]", (msg.get("content") or "").strip())


if __name__ == "__main__":
    main()

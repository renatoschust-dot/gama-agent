<div align="center">

# 🟣 GAMA Agent 35B

**Open-source Bosnian agent / tool-calling LLM — a fine-tune of Qwen3.5-35B-A3B (MoE).**

[![made by gamAI](https://img.shields.io/badge/made%20by-gamAI-6E56CF)](https://gamai.io)
[![license](https://img.shields.io/badge/license-Apache--2.0-green)](./LICENSE)
[![base](https://img.shields.io/badge/base-Qwen3.5--35B--A3B-blueviolet)](https://huggingface.co/Qwen/Qwen3.5-35B-A3B)
[![GGUF](https://img.shields.io/badge/GGUF-Q4__K__M%20~21GB-orange)](https://huggingface.co/renatoschust/gama-agent)

🤗 **Model (GGUF):** [huggingface.co/renatoschust/gama-agent](https://huggingface.co/renatoschust/gama-agent) ·
🧩 **LoRA adapter:** [huggingface.co/renatoschust/gama-agent-lora](https://huggingface.co/renatoschust/gama-agent-lora) ·
🌐 **gamAI:** [gamai.io](https://gamai.io)

</div>

---

## What is this?

**GAMA Agent 35B** is a **Bosnian** (HR/SR/EN) language model tuned to **act, not just chat**.
Given a task and a list of tools, it emits structured **tool calls** so it can drive software,
query databases, run commands, and complete multi-step jobs (diagnose → act → verify).

It is a fine-tune of **Qwen3.5-35B-A3B** (Mixture-of-Experts: ~35B total, ~3B active),
shipped as a ready-to-run **GGUF Q4_K_M (~21 GB)** quantisation.

Built by **[gamAI](https://gamai.io)** — an open AI toolkit.

## Highlights

| | |
|---|---|
| 🧠 **Base** | Qwen3.5-35B-A3B (MoE, ~35B total / ~3B active) |
| 🎯 **Tuning** | SFT + DPO agent tuning (LoRA r=16, α=16) |
| 📦 **Format** | GGUF `Q4_K_M` (~21 GB) |
| 🗣️ **Languages** | Bosnian (primary), Croatian, Serbian, English |
| 🪟 **Context** | up to 32k tokens |
| 🛡️ **Safety** | refuses destructive actions (`rm -rf`, dropping a DB, deleting logs) |

## Capabilities

- **Bosnian conversation** — fluent, natural (ijekavica / latinica).
- **Tool / function calling** — structured tool calls (JSON) for shell, file I/O, service status, SQL, HTTP, calculations.
- **Multi-step agent tasks** — plan → act → verify loops from a single instruction.
- **Safety first** — refuses destructive operations instead of executing them.
- **Non-thinking** — direct answers, low latency.

## Quickstart

### Ollama
```bash
ollama run hf.co/renatoschust/gama-agent
```

### llama.cpp (`llama-server`, OpenAI-compatible API)
```bash
llama-server -hf renatoschust/gama-agent -c 32768 --port 8080

curl http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '{
  "messages":[{"role":"user","content":"Koliko je 15% od 240?"}],
  "temperature":0
}'
```

### LM Studio / GPT4All
Download the GGUF and load it directly.

## Tool-calling

Pass tools using the standard OpenAI `tools` schema and keep `temperature` low (0–0.2).
Example system prompt:

```
Ti si asistent. Za svaki zahtjev koji traži stanje sistema ili akciju koristi odgovarajući alat (function call).
Ako zahtjev traži opasnu ili razornu akciju (brisanje, formatiranje, gašenje), ODBIJ i ne pozivaj alat.
Ako je pitanje opće prirode, odgovori normalno bez poziva alata.
```

See [`examples/tool_call.py`](./examples/tool_call.py) for a runnable example.

## Training data

Trained on **synthetic, placeholder-sanitised** Bosnian agent traces (function-calling,
terminal/ops trajectories, confirmation/rebalance and DPO preference pairs).
**No real customer, company or personal data was used.**

## Limitations

- **Bosnian-first** — quality drops on other languages.
- **~21 GB** — needs a machine with sufficient RAM/VRAM (a 24 GB GPU, or ≥24 GB RAM with offload).
- Agent reliability depends on the tool schema and system prompt you provide.
- Not a knowledge base — ground it with retrieval (RAG) for facts.
- Keep a human gate on destructive operations.

## License

[Apache-2.0](./LICENSE) — inherited from the Qwen3.5-35B-A3B base model.

---

<div align="center">
Built with ❤️ by <a href="https://gamai.io"><b>gamAI</b></a> — open AI toolkit
</div>

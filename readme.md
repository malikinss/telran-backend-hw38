# Homework 38 – LTR Evaluation Agent Integration

## Task Definition

The goal of Homework 38 is to **enhance an LLM-based agent** by integrating a **left-to-right (LTR) arithmetic evaluation tool** and updating agent behavior.

Specifically, the task requires:

1. Integrating the code for calculating arithmetic expressions from Homework #36 into the agent.
2. Updating the agent CLI and core agent classes.
3. Adding a tool for **LTR evaluation** (`ltr_evaluate(expr: string)`).
4. Modifying the system prompt to enforce **strict tool-routing** rules.
5. Ensuring that when LTR evaluation is applied, **only the evaluation result** is returned in the response.

---

## 📝 Description

This project implements a **Python agent capable of routing user requests to external tools**, with special focus on **arithmetic evaluation**.

Key components:

- **`ToolAgent` class** – Core agent managing conversation, detecting tool requests, executing tools, and returning results.
- **`AgentCLI` class** – Command-line interface for interacting with the agent with a dynamic "thinking" indicator.
- **`LTR evaluation tool` (`LtrCalculator`)** – Evaluates arithmetic expressions strictly left-to-right, ignoring operator precedence.
- **`ToolRouter`** – Extracts tool invocation requests from LLM responses and executes corresponding tools.
- **System prompt** – Defines agent behavior, available tools, and strict JSON output rules.

Project structure:

```

./src/
├─ agent/                 # Core agent and CLI
│   ├─ agent.py           # ToolAgent implementation
│   ├─ cli.py             # CLI interface
│   ├─ llm.py             # Phi-3 API wrapper
│   └─ common_data_types.py
├─ tools/                 # Tool implementations
│   ├─ ltr/               # Left-to-right arithmetic evaluation
│   ├─ weather/           # Weather API (optional)
│   ├─ tools.py           # Base tool class and registry
│   └─ tool_router.py     # Tool extraction and execution
├─ config/                # System configuration
│   └─ system_content.py  # Agent rules and prompts
├─ utils/                 # Utility functions
│   └─ thinking_dots.py   # "Thinking..." indicator for CLI
└─ main.py                # Entry point for CLI

```

---

## 🎯 Purpose

The homework focuses on:

1. **Tool integration** – Adding LTR evaluation as a callable tool.
2. **Agent architecture** – Implementing an LLM-driven agent that can route requests to tools.
3. **Strict output formatting** – JSON-only tool outputs to maintain consistency.
4. **Testing and reliability** – Ensuring evaluation results are correctly calculated and returned.

This ensures the agent can handle **real-time user input** and **perform computation reliably**.

---

## 🔍 How It Works

1. **Initialization**
    - `AgentCLI` loads environment variables and starts the `ToolAgent`.
    - `ToolAgent` initializes `LLMClient` and `ToolRouter`.
    - System prompt enforces tool usage rules.

2. **Processing User Input**
    - User input is appended to conversation history.
    - `ToolAgent` queries Phi-3 API via `LLMClient`.
    - Response is analyzed for JSON instructions specifying a tool call.

3. **Tool Invocation**
    - `ToolRouter` extracts tool name and arguments from JSON.
    - Registered tools (`ltr_evaluate` or `get_weather`) are executed.
    - Only tool output is returned if required.

4. **LTR Evaluation**
    - Expression is validated for syntax and parentheses.
    - Parentheses are recursively resolved.
    - Final expression is evaluated strictly left-to-right ignoring precedence.

5. **Output**
    - Agent responds with either natural language or JSON tool output.
    - Tool outputs are strictly **JSON only**, with no extra text.

---

## 📜 Output Example

### ✅ LTR Evaluation

```py
You: 2 + 2 * 3
Agent: 12
```

### ✅ Nested Parentheses

```py
You: (2 + 2) * 3
Agent: 12
```

### ❌ Invalid Expression

```py
You: 2 + *
Agent: [Error calling tool ltr_evaluate: Syntax error in expression: 2 + *]
```

---

## 📦 Usage

```py
from src.main import main

if __name__ == "__main__":
    main()
```

- Start the CLI: type arithmetic expressions to evaluate.
- Type `exit` to quit the session.
- LTR evaluation is triggered automatically for raw arithmetic expressions.

---

## ✅ Dependencies

- Python 3.10+
- `requests` library
- `python-dotenv` (for environment variables)
- Phi-3 API access credentials (`PHI3_API_URL`, `PHI3_MODEL_NAME`)

---

## 📊 Project Status

**Status:** ✅ Completed

- Agent capable of routing tool requests integrated with CLI.
- LTR arithmetic evaluation fully implemented.
- JSON-only tool output strictly enforced.
- Robust error handling for invalid expressions.

---

## 📄 License

MIT License

---

## 🧮 Conclusion

This project demonstrates **advanced agent-tool integration** in Python with:

- Structured LLM-agent design (`ToolAgent`, `ToolRouter`, `LLMClient`),
- Robust arithmetic evaluation (LTR, parentheses handling, syntax validation),
- Clear separation between tool logic and agent conversation,
- Real-time, reliable command-line interaction.

---

Made with ❤️ and `Python` by **Sam-Shepsl Malikin** 🎓

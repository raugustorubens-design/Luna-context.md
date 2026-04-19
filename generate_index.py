# 🧠 LUNA INDEX ENGINE v2.1

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv",
    "venv", "dist", "build"
}

VALID_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".md"
}

OUTPUT_JSON = "luna_context.json"
STATE_FILE = ".luna_state.json"


# 🔐 HASH (detecção de mudança)
def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def is_valid_file(file_path):
    return (
        file_path.suffix in VALID_EXTENSIONS
        and not any(part in IGNORE_DIRS for part in file_path.parts)
    )


def extract_luna_comment(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for _ in range(20):
                line = f.readline()
                if "@luna:" in line.lower():
                    return line.split(":", 1)[1].strip()
    except:
        pass
    return None


def infer_purpose(file_path):
    name = file_path.name.lower()

    if "main" in name or "app" in name:
        return "Entrypoint"
    if "route" in name or "api" in name:
        return "API"
    if "service" in name:
        return "Service"
    if "model" in name:
        return "Data Model"
    if "config" in name:
        return "Config"
    if "worker" in name:
        return "Worker"
    if "test" in name:
        return "Test"
    return "Unknown"


# 📦 LOAD STATE
def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# 🧠 INDEX + TRACE (ΔE real)
def generate_index_and_trace(root):
    previous = load_previous_state()
    current = {}
    index = []
    trace = []

    for path in Path(root).rglob("*"):
        if path.is_file() and is_valid_file(path):
            rel = str(path.relative_to(root))
            h = file_hash(path)

            current[rel] = h

            luna_comment = extract_luna_comment(path)
            purpose = luna_comment or infer_purpose(path)

            index.append({
                "file": rel,
                "purpose": purpose,
                "hash": h
            })

            # 🍞 ΔE DETECTION
            if rel not in previous:
                trace.append({
                    "file": rel,
                    "action": "created",
                    "result": purpose
                })
            elif previous[rel] != h:
                trace.append({
                    "file": rel,
                    "action": "modified",
                    "result": "content changed"
                })

    # deletions
    for old_file in previous:
        if old_file not in current:
            trace.append({
                "file": old_file,
                "action": "deleted",
                "result": "removed from project"
            })

    return index, trace, current


# 🧠 CHECKPOINT
def generate_checkpoint(trace):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "estado": "Projeto indexado com detecção de mudanças",
        "trajetoria": [t["action"] for t in trace],
        "aprendizado": [
            "mudanças são detectadas via hash",
            "estrutura evolui continuamente"
        ],
        "proximo_passo": "refinar semântica com @luna"
    }


# 💾 SAVE CONTEXT
def save_context(index, trace, checkpoint):
    data = {
        "system": "LUNA",
        "version": "2.1",
        "memory": {
            "LTM": index,
            "TRACE": trace,
            "CHECKPOINT": checkpoint
        }
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# 🚀 RUN
if __name__ == "__main__":
    root = "."

    index, trace, state = generate_index_and_trace(root)
    checkpoint = generate_checkpoint(trace)

    save_context(index, trace, checkpoint)
    save_state(state)

    print("🧠 LUNA Context atualizado com TRACE real + CHECKPOINT")

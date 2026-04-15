# Luna-context.md
import os
from pathlib import Path

# Diretórios que devem ser ignorados
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build"
}

# Extensões relevantes
VALID_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".md"
}

OUTPUT_FILE = "LUNA_INDEX.md"


def is_valid_file(file_path):
    return (
        file_path.suffix in VALID_EXTENSIONS
        and not any(part in IGNORE_DIRS for part in file_path.parts)
    )


def extract_luna_comment(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for _ in range(20):  # lê só o topo do arquivo
                line = f.readline()
                if not line:
                    break
                if "@luna:" in line.lower():
                    return line.split(":", 1)[1].strip()
    except:
        return None
    return None


def infer_purpose(file_path):
    name = file_path.name.lower()

    if "main" in name or "app" in name:
        return "Entrypoint da aplicação"
    if "route" in name or "api" in name:
        return "Definição de rotas/API"
    if "service" in name:
        return "Lógica de serviço"
    if "model" in name:
        return "Modelo de dados"
    if "config" in name:
        return "Configuração do sistema"
    if "worker" in name:
        return "Execução de tarefas/ações"
    if "test" in name:
        return "Testes"
    return "Função não documentada"


def generate_index(root_path):
    index = []

    for path in Path(root_path).rglob("*"):
        if path.is_file() and is_valid_file(path):
            relative_path = path.relative_to(root_path)

            luna_comment = extract_luna_comment(path)

            purpose = luna_comment if luna_comment else infer_purpose(path)

            index.append((str(relative_path), purpose))

    index.sort()

    return index


def write_markdown(index):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# 🧠 LUNA INDEX\n\n")
        f.write("Mapa automático do projeto.\n\n")

        current_folder = None

        for path, purpose in index:
            folder = os.path.dirname(path)

            if folder != current_folder:
                current_folder = folder
                f.write(f"\n## 📁 {folder if folder else 'root'}\n\n")

            f.write(f"- **{os.path.basename(path)}** → {purpose}\n")


if __name__ == "__main__":
    root = "."
    index = generate_index(root)
    write_markdown(index)

    print(f"✅ Índice gerado com sucesso em {OUTPUT_FILE}")

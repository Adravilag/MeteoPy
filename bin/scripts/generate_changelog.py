import subprocess
from datetime import date
import os

print("Iniciando la generación del changelog...")  # Mensaje de inicio

def get_git_tags():
    print("Obteniendo etiquetas de Git...")
    result = subprocess.run(["git", "tag"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al obtener etiquetas de Git:", result.stderr)
        return []
    return result.stdout.splitlines()

def get_git_log(min_tag=None):
    print("Obteniendo logs de Git...")
    command = ["git", "log", "--pretty=format:%h - %s"]
    if min_tag:
        command.append(f"{min_tag}..HEAD")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al obtener logs de Git:", result.stderr)
        return []
    return result.stdout.splitlines()

def get_git_diff(commit_hash):
    print(f"Obteniendo diferencias completas para el commit {commit_hash}...")
    result = subprocess.run(["git", "diff", f"{commit_hash}~1", commit_hash], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al obtener diferencias de Git:", result.stderr)
        return ""
    return result.stdout  # No limitamos el contenido, obtenemos el diff completo

def generate_changelog_content(min_tag):
    commits = get_git_log(min_tag)
    if not commits:
        print("No se encontraron commits recientes.")
        return "No se encontraron commits recientes."

    changelog = "Changelog generado:\n\n"
    for commit in commits:
        commit_hash, commit_message = commit.split(" - ", 1)
        diff_content = get_git_diff(commit_hash)
        changelog += f"Commit Message: {commit_message}\n"
        changelog += f"Changes:\n{diff_content}\n\n"
    
    return changelog

def save_changelog(content):
    filename = f"changelog_{date.today()}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Changelog guardado en {filename}")

# Obtener la versión mínima a partir de la cual generar el changelog
tags = get_git_tags()
if len(tags) > 1:
    min_tag = tags[-2]  # Penúltima etiqueta
else:
    min_tag = None
print(f"Penúltimo tag encontrado: {min_tag}")

# Generar el contenido del changelog sin la API de OpenAI
changelog_content = generate_changelog_content(min_tag)
print("Resultado del changelog:\n")
print(changelog_content)  # Imprimir el changelog en la consola
save_changelog(changelog_content)  # Guardar el changelog en un archivo

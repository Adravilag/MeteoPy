import subprocess
import os
from datetime import date
from dotenv import load_dotenv
import openai
import time

# Cargar la API Key de OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print("Iniciando la generación del changelog...")  # Mensaje de inicio

def get_git_tags():
    # Obtener etiquetas de Git
    print("Obteniendo etiquetas de Git...")
    result = subprocess.run(
        ["git", "tag"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error al obtener etiquetas de Git:", result.stderr)
        return []
    return result.stdout.splitlines()

def get_git_log(min_tag=None):
    # Obtener commits recientes
    print("Obteniendo logs de Git...")
    command = ["git", "log", "--pretty=format:%h - %s"]
    
    if min_tag:
        command.append(f"{min_tag}..HEAD")  # Usar la etiqueta para limitar los commits
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al obtener logs de Git:", result.stderr)
        return []
    return result.stdout.splitlines()

def get_git_diff(commit_hash):
    # Obtener los cambios de un commit específico usando git diff
    print(f"Obteniendo diferencias para el commit {commit_hash}...")
    result = subprocess.run(
        ["git", "diff", f"{commit_hash}~1", commit_hash],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error al obtener diferencias de Git:", result.stderr)
        return ""
    return result.stdout

def summarize_diff(diff_content):
    # Resumir el diff, aquí simplemente limitamos a los primeros 500 caracteres
    return diff_content[:500]

def generate_prompt_with_changes(limit=10, min_tag=None):
    commits = get_git_log(min_tag)
    if not commits:
        print("No se encontraron commits recientes.")
        return "No se encontraron commits recientes."

    # Limitar a los últimos 'limit' commits
    commits = commits[:limit]
    prompt = "Generate a changelog based on the following commits and changes:\n\n"
    
    for commit in commits:
        commit_hash, commit_message = commit.split(" - ", 1)
        diff_content = summarize_diff(get_git_diff(commit_hash))

        prompt += f"Commit Message: {commit_message}\n"
        prompt += f"Changes:\n{diff_content}\n\n"
    
    return prompt

def improve_changelog(prompt):
    # Usar GPT para generar el changelog basado en el prompt
    while True:  # Intentar hasta que se complete correctamente
        try:
            print("Generando changelog utilizando la API de OpenAI...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates changelogs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=5000
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Waiting for 120 seconds before retrying...")
            time.sleep(120)  # Esperar 120 segundos antes de reintentar
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break  # Salir del bucle en caso de un error inesperado

def save_changelog(content):
    # Guardar el changelog generado
    filename = f"changelog_{date.today()}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Changelog saved to {filename}")

# Obtener la versión mínima a partir de la cual generar el changelog
tags = get_git_tags()
print("Etiquetas disponibles:", tags)
min_tag = input("Introduce la versión mínima (etiqueta de Git) a partir de la cual generar el changelog: ")

# Verificar si la API key está configurada
if openai.api_key:
    prompt = generate_prompt_with_changes(min_tag=min_tag)
    print("Prompt generado:", prompt)  # Imprimir el prompt para depuración
    changelog = improve_changelog(prompt)
    save_changelog(changelog)
else:
    print("Warning: OPENAI_API_KEY is not set. Generating a basic changelog based on git commits only.")
    changelog = generate_prompt_with_changes(min_tag=min_tag)
    save_changelog(changelog)

import os
import git
import requests

# Configura tus variables
repo_name = ''  # Cambia esto al nombre de tu repositorio
username = ''  # Cambia esto a tu nombre de usuario de GitHub
token = ''  # Cambia esto a tu token de acceso personal de GitHub
repo_path = ''  # Cambia esto a la ruta de tu repositorio local
commit_message = 'Subiendo cambios a GitHub'

# Función para crear un repositorio en GitHub
def crear_repositorio():
    url = f'https://api.github.com/user/repos'
    headers = {'Authorization': f'token {token}'}
    data = {'name': repo_name}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f'Repositorio "{repo_name}" creado exitosamente.')
    else:
        print(f'Error al crear el repositorio: {response.json()}')

try:
    # Cambia al directorio del repositorio
    os.chdir(repo_path)

    # Inicializa el repositorio si no existe
    if not os.path.exists(os.path.join(repo_path, '.git')):
        repo = git.Repo.init(repo_path)
        crear_repositorio()  # Crea el repositorio en GitHub
    else:
        repo = git.Repo(repo_path)

    # Agrega todos los cambios
    repo.git.add(A=True)

    # Realiza un commit
    repo.index.commit(commit_message)

    # Crea la rama 'main' si no existe
    if 'main' not in repo.heads:
        repo.git.checkout('-b', 'main')

    # Configura la URL remota
    remote_url = f'https://github.com/{username}/{repo_name}.git'
    if 'origin' not in repo.remotes:
        repo.create_remote('origin', remote_url)

    # Sube los cambios a la rama principal
    repo.git.push('origin', 'main')  # Cambia 'main' a 'master' si es necesario

except Exception as e:
    print(f'Ocurrió un error: {e}')

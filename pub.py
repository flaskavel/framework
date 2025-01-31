import os
import shutil
import subprocess
import sys
from flaskavel.metadata import VERSION

# 🔄 Asegura que todo se ejecuta en la ruta donde se corre el script
WORKING_DIR = os.getcwd()

def clear_project():
    """
    Elimina las carpetas de compilación generadas por setup.py.
    """
    folders = ["build", "dist", "flaskavel.egg-info"]
    for folder in folders:
        folder_path = os.path.join(WORKING_DIR, folder)
        if os.path.exists(folder_path):
            print(f"🗑️ Eliminando {folder}...")
            try:
                shutil.rmtree(folder_path)
            except PermissionError:
                print(f"❌ Error: No se pudo eliminar {folder} por permisos.")
            except Exception as e:
                print(f"❌ Error eliminando {folder}: {str(e)}")

def git():
    """
    Verifica si hay cambios en Git, los comitea y los sube al repositorio remoto.
    """
    git_status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=WORKING_DIR)
    modified_files = git_status.stdout.strip()

    if modified_files:
        print("📌 Agregando archivos al commit...")
        subprocess.run(["git", "add", "."], check=True, cwd=WORKING_DIR)

        print(f"✅ Realizando commit: '📦 Release version {VERSION}'")
        subprocess.run(["git", "commit", "-m", f"📦 Release version {VERSION}"], check=True, cwd=WORKING_DIR)

        print("🚀 Pushing al repositorio remoto...")
        subprocess.run(["git", "push", "-f"], check=True, cwd=WORKING_DIR)
    else:
        print("✅ No hay cambios para comitear.")

def build():
    """
    Compila el paquete usando setup.py y genera archivos de distribución.
    """
    python_path = sys.executable  # 🐍 Detecta el Python actual

    setup_path = os.path.join(WORKING_DIR, "setup.py")
    if not os.path.exists(setup_path):
        print("❌ Error: setup.py no encontrado en el directorio actual.")
        return

    print("⚙️ Compilando el proyecto...")
    subprocess.run([python_path, "setup.py", "sdist", "bdist_wheel"], check=True, cwd=WORKING_DIR)
    print("✅ Build completado.")

def publish():
    """
    Publica el paquete en PyPI usando Twine.
    """
    token = os.getenv("PYPI_TOKEN")  # 🔒 Usa variable de entorno
    if not token:
        print("❌ Error: PyPI_TOKEN no encontrado en las variables de entorno.")
        return

    twine_path = os.path.join(os.path.dirname(sys.executable), "twine")  # 🛠️ Encuentra Twine automáticamente

    if not os.path.exists(twine_path):
        print(f"❌ Error: Twine no encontrado en {twine_path}. Instala con `pip install twine`")
        return

    print("📤 Subiendo el paquete a PyPI...")
    subprocess.run([twine_path, "upload", "dist/*", "-u", "__token__", "-p", token], check=True, cwd=WORKING_DIR)

    # 🧹 Limpieza de archivos temporales
    print("🧹 Eliminando archivos .pyc y __pycache__...")
    subprocess.run(["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"], check=True, cwd=WORKING_DIR, shell=True)
    
    print("✅ ¡Publicación completada exitosamente!")

# 🚀 Ejecutar el script
if __name__ == "__main__":
    try:
        git()
        clear_project()
        build()
        publish()
    except Exception as e:
        print(f"❌ Error General: {e}")
    finally:
        clear_project()

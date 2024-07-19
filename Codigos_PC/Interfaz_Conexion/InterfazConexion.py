import paramiko
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar, messagebox
import json
import os

# Directorio del script actual
current_dir = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(current_dir, 'config.json')
icon_path = os.path.join(current_dir, "wifi_icon.ico")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'raspberry_pi_ip': '192.168.4.1',
            'username': 'pi',
            'password': 'raspberry',
            'remote_file_path': '/home/pi/Codigos_Raspberry/Archivos'
        }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def compress_folder(remote_folder_path, compressed_file_path, ssh_client):
    command = f"tar -czf {compressed_file_path} -C {remote_folder_path} ."
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()  # Wait for the command to finish
    if exit_status != 0:
        raise Exception(f"Error compressing folder: {stderr.read().decode()}")

def download_folder(remote_folder_path, local_folder_path, config):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config['raspberry_pi_ip'], username=config['username'], password=config['password'])
    
    compressed_file_path = f"/tmp/{os.path.basename(remote_folder_path)}.tar.gz"
    compress_folder(remote_folder_path, compressed_file_path, ssh)
    
    sftp = ssh.open_sftp()
    local_compressed_file_path = os.path.join(local_folder_path, os.path.basename(compressed_file_path))
    sftp.get(compressed_file_path, local_compressed_file_path)
    sftp.close()
    ssh.close()
    
    # Extract the downloaded tar.gz file
    import tarfile
    with tarfile.open(local_compressed_file_path, "r:gz") as tar:
        tar.extractall(path=local_folder_path)
    
    # Remove the local compressed file after extraction
    os.remove(local_compressed_file_path)

def select_folder():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    folder_selected = filedialog.askdirectory()
    return folder_selected

def main():
    config = load_config()

    def save_and_exit():
        config['raspberry_pi_ip'] = raspberry_pi_ip.get()
        config['username'] = username.get()
        config['password'] = password.get()
        config['remote_file_path'] = remote_file_path.get()
        save_config(config)
        root.destroy()
        
    def download():
        destination_folder = select_folder()
        if not destination_folder:
            print("No se seleccionó ninguna carpeta.")
            return
        
        try:
            download_folder(config['remote_file_path'], destination_folder, config)
            messagebox.showinfo("Información", f"Carpeta descargada y extraída en: {destination_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error: {e}")

    root = Tk()
    root.title("Configuración Raspberry Pi")
    root.iconbitmap(icon_path)
    root.geometry("325x225")

    padding = 10

    Label(root, text="IP de Raspberry Pi:").grid(row=0, column=0, sticky="e", padx=padding, pady=padding)
    Label(root, text="Usuario:").grid(row=1, column=0, sticky="e", padx=padding, pady=padding)
    Label(root, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=padding, pady=padding)
    Label(root, text="Ruta de archivo remoto:").grid(row=3, column=0, sticky="e", padx=padding, pady=padding)

    raspberry_pi_ip = StringVar(value=config['raspberry_pi_ip'])
    username = StringVar(value=config['username'])
    password = StringVar(value=config['password'])
    remote_file_path = StringVar(value=config['remote_file_path'])

    Entry(root, textvariable=raspberry_pi_ip).grid(row=0, column=1, padx=padding, pady=padding)
    Entry(root, textvariable=username).grid(row=1, column=1, padx=padding, pady=padding)
    Entry(root, textvariable=password, show='*').grid(row=2, column=1, padx=padding, pady=padding)
    Entry(root, textvariable=remote_file_path).grid(row=3, column=1, padx=padding, pady=padding)

    Button(root, text="Guardar y Salir", command=save_and_exit).grid(row=4, column=0, padx=padding, pady=padding)
    Button(root, text="Descargar Archivo", command=download).grid(row=4, column=1, padx=padding, pady=padding)

    root.mainloop()

if __name__ == "__main__":
    main()

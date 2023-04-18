import tkinter as tk
import requests
import socket
from tkinter import filedialog
import telnetlib
import subprocess


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(bg='gray')  # define a cor de fundo
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="SERVER:")
        self.url_label.grid(row=2, column=0, pady=5)

        self.url_entry = tk.Entry(self)
        self.url_entry.grid(row=2, column=1, pady=5)

        self.ports_label = tk.Label(self, text="Port Range (start-end):")
        self.ports_label.grid(row=3, column=0, pady=5)

        self.ports_entry = tk.Entry(self)
        self.ports_entry.grid(row=3, column=1, pady=5)

        self.tracert_button = tk.Button(self, text="Tracert", command=self.tracertbutton, width=15, bg="#00FFFF")
        self.tracert_button.grid(row=2, column=3, sticky="E")

        self.telnet_button = tk.Button(self, text="Telnet",command=self.telnet_button, width=15, bg="#00FFFF")
        self.telnet_button.grid(row=3, column=3, sticky="E")

        self.listeners_button = tk.Button(self, text="Test Listeners", command=self.test_listeners, width=15, bg="#00FFFF")
        self.listeners_button.grid(row=5, column=3, sticky="E")

        self.results_text = tk.Text(self)
        self.results_text.grid(row=6, columnspan=4)

        self.clear_button = tk.Button(self, text="Clear log", command=self.clear_logs, width=15, bg="#00FFFF")
        self.clear_button.grid(row=7, column=2, sticky="E")

        self.telnet_button = tk.Button(self, text="Save log", width=15, bg="#00FFFF", command=self.save_file)
        self.telnet_button.grid(row=7, column=3, sticky="E")

    def clear_logs(self):
        self.results_text.delete(1.0, tk.END)

    def test_listeners(self):
        url = self.url_entry.get()
        if url:
            ports = self.ports_entry.get().split("-")
            if len(ports) == 2:
                start_port = int(ports[0])
                end_port = int(ports[1])
                for port in range(start_port, end_port + 1):
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(0.5)
                            s.connect((url, port))
                        self.results_text.insert(tk.END, f"Port {port} is listening\n")
                    except:
                        self.results_text.insert(tk.END, f"Port {port} is not listening\n")

    def save_file(self):
        # Abre janela de diálogo para selecionar o diretório
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if not file_path:
            # Usuário cancelou a seleção
            return
        with open(file_path, 'w') as f:
            f.write(self.results_text.get('1.0', 'end-1c'))

    def telnet_button(self):
        # Obtem as informações do formulário
        server = self.url_entry.get()
        port = int(self.ports_entry.get())

        # Tenta se conectar via telnet
        try:
            tn = telnetlib.Telnet(server, port)

            # Executa um comando simples para verificar se a conexão foi bem sucedida
            tn.write(b'ls\n')
            response = tn.read_until(b'# ').decode('ascii')

            # Atualiza o campo de texto com a resposta
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Conexão bem sucedida!\n\n{response}")
        except Exception as e:
            # Em caso de erro, atualiza o campo de texto com uma mensagem de erro
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Erro ao conectar ao servidor: {str(e)}")

    def tracertbutton(self):
        address = self.url_entry.get()
        process = subprocess.Popen(["tracert", address], stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, output.decode('iso-8859-1'))


root = tk.Tk()
app = Application(master=root)
app.mainloop()

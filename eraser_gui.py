import os
import threading
from tkinter import filedialog
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from eraser import BackgroundEraser

class App(ctk.CTk):
    """
    Aplicación gráfica para eliminar fondos de imágenes usando la librería rembg.
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal, configura la apariencia y crea los componentes UI.
        """
        super().__init__()
        self.title("Background Eraser")
        self.geometry("600x200")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 200) // 2
        self.geometry(f"+{x}+{y}")

        self.input_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Crea y organiza todos los elementos gráficos de la interfaz.
        """
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        self.input_label = ctk.CTkLabel(self.input_frame, text="Imagen de entrada:")
        self.input_label.pack(side="left", padx=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, textvariable=self.input_path, state="readonly")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.input_btn = ctk.CTkButton(
            self.input_frame,
            text="Seleccionar",
            fg_color="#FF6B6B",
            hover_color="#FF4C4C",
            corner_radius=12,
            command=self.select_input
        )
        self.input_btn.pack(side="right", padx=5)

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=20, fill="x")

        self.output_label = ctk.CTkLabel(self.output_frame, text="Directorio de salida:")
        self.output_label.pack(side="left", padx=5)

        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_dir, state="readonly")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.output_btn = ctk.CTkButton(
            self.output_frame,
            text="Seleccionar",
            fg_color="#FF6B6B",
            hover_color="#FF4C4C",
            corner_radius=12,
            command=self.select_output
        )
        self.output_btn.pack(side="right", padx=5)

        self.process_btn = ctk.CTkButton(
            self,
            text="Eliminar Fondo",
            fg_color="#2E8B57",
            hover_color="#3CB371",
            corner_radius=15,
            command=self.start_processing
        )
        self.process_btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def select_input(self):
        """
        Abre un diálogo para seleccionar la imagen de entrada y actualiza la UI.
        """
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.input_path.set(path)

    def select_output(self):
        """
        Abre un diálogo para seleccionar el directorio de salida y actualiza la UI.
        """
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def start_processing(self):
        """
        Inicia el procesamiento en segundo plano tras validar las rutas seleccionadas.
        """
        input_path = self.input_path.get()
        output_dir = self.output_dir.get()

        if not input_path or not output_dir:
            CTkMessagebox(title="Error", message="Selecciona ambos archivos y directorio", icon="cancel")
            return

        self.process_btn.configure(state="disabled")
        self.status_label.configure(text="Procesando...")

        thread = threading.Thread(target=self.process_image, args=(input_path, output_dir))
        thread.start()

    def process_image(self, input_path, output_dir):
        """
        Ejecuta el proceso de eliminación de fondo y gestiona las respuestas de la UI.
        
        Args:
            input_path (str): Ruta de la imagen de entrada.
            output_dir (str): Directorio donde se guardará la imagen procesada.
        """
        try:
            eraser = BackgroundEraser(input_folder="", output_folder=output_dir)
            eraser.process_single_image(input_path, output_dir)
            
            self.after(0, lambda: CTkMessagebox(
                title="Éxito",
                message="¡Fondo eliminado correctamente!",
                icon="check"
            ))
        except Exception as e:
            self.after(0, lambda: CTkMessagebox(
                title="Error",
                message=f"Error: {str(e)}",
                icon="cancel"
            ))
        finally:
            self.after(0, lambda: [
                self.process_btn.configure(state="normal"),
                self.status_label.configure(text="")
            ])

if __name__ == "__main__":
    app = App()
    app.mainloop()

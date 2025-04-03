import os
from datetime import datetime
from rembg import remove

class BackgroundEraser:
    """
    Clase para eliminar fondos de imágenes y gestionar archivos procesados.
    """
    
    def __init__(self, input_folder, output_folder):
        """
        Inicializa la clase con las rutas de entrada y salida.

        Args:
            input_folder (str): Carpeta donde se encuentran las imágenes originales.
            output_folder (str): Carpeta base donde se guardarán los resultados.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self):
        """
        Procesa todas las imágenes en la carpeta de entrada:
        1. Crea una carpeta con la fecha actual en la salida
        2. Elimina el fondo de cada imagen
        3. Mueve los originales a una subcarpeta 'originals'
        """
        today_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        processed_folder = os.path.join(self.output_folder, today_date)
        os.makedirs(processed_folder, exist_ok=True)

        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(self.input_folder, filename)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_without-bg{ext}"
                output_path = os.path.join(processed_folder, new_filename)

                self.remove_background(input_path, output_path)
                self.move_originals(input_path, processed_folder)

    def process_single_image(self, input_path, output_folder):
        """
        Procesa una única imagen y la guarda en la carpeta especificada.

        Args:
            input_path (str): Ruta completa de la imagen a procesar.
            output_folder (str): Carpeta base donde se guardará el resultado.
        """
        today_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        processed_folder = os.path.join(output_folder, today_date)
        os.makedirs(processed_folder, exist_ok=True)
        
        name, ext = os.path.splitext(os.path.basename(input_path))
        new_filename = f"{name}_without-bg{ext}"
        output_path = os.path.join(processed_folder, new_filename)
        
        self.remove_background(input_path, output_path)
        self.move_originals(input_path, processed_folder)

    def remove_background(self, input_p, output_p):
        """
        Elimina el fondo de una imagen usando la librería rembg.

        Args:
            input_p (str): Ruta de la imagen original.
            output_p (str): Ruta donde se guardará la imagen procesada.
        """
        with open(input_p, "rb") as inp, open(output_p, "wb") as out:
            background_output = remove(inp.read())
            out.write(background_output)

    def move_originals(self, input_p, dest_p):
        """
        Mueve la imagen original a una carpeta 'originals' dentro del destino.

        Args:
            input_p (str): Ruta de la imagen original.
            dest_p (str): Carpeta destino donde se creará la subcarpeta.
        """
        originals_folder = os.path.join(dest_p, "originals")
        os.makedirs(originals_folder, exist_ok=True)

        filename = os.path.basename(input_p)
        new_path = os.path.join(originals_folder, filename)
        os.rename(input_p, new_path)
import os, json
import tkinter as tk
from tkinter import ttk, messagebox

from cfgparser import cfgparser as cp
from cfgparser.config import kahoot_to_classroom
from translator import fetcher as fc
from translator import translator as tr
from translator import saver as sv
from interface.factories import TitleBar, LabelFactory, ButtonFactory, DropdownFactory, ProgressFactory, StatusLabelFactory

from config import *

cp_cfg = kahoot_to_classroom()

# --- GUI principal ---
class AppGUI(tk.Tk):
    def __init__(self, settings, template):
        super().__init__()

        # Estructura del GUI
        self.labels    = template[LABELS]
        self.dropdowns = template[DROPDOWNS]
        self.buttons   = template[BUTTONS]

        # Configuraciones
        self.window_cfg   = settings[WINDOW]
        self.titlebar_cfg = settings[TITLEBAR]
        self.frame_cfg    = settings[FRAME]
        self.label_cfg    = settings[LABEL]
        self.dropdown_cfg = settings[DROPDOWN]
        self.button_cfg   = settings[BUTTON]
        self.progress_cfg = settings[PROGRESS]
        self.status_cfg   = settings[STATUS]

        # Factories (cada uno recibe su sección del JSON)
        self.label_factory    = LabelFactory(self.label_cfg)
        self.dropdown_factory = DropdownFactory(self.dropdown_cfg)
        self.button_factory   = ButtonFactory(self.button_cfg)
        self.progress_factory = ProgressFactory(self.progress_cfg)

        self.create_window()
        self.center_window()
        self.overrideredirect(True)
        self.build_section("config", "dropdown")
        self.build_section("report", "dropdown")
        self.build_section("convert", "button")
        self.build_section("progress_status", "status")

    def build_section(self, section_name, section_type):
        """Construye una sección según su tipo declarativo."""
        if section_type == "dropdown":
            # Label
            self.label_factory.create(
                parent=self.frame,
                text=self.labels[section_name]["text"]
            ).pack(pady=5, anchor="w")

            # Archivos y variable
            folder = "config" if section_name == "config" else "reports"
            ext    = ".ini" if section_name == "config" else ".xlsx"
            files  = self.get_files(folder=folder, ext=ext)
            var    = tk.StringVar(value=files[0] if files else "")

            if section_name == "config":
                self.selected_config = var
                self.config_dropdown = self.dropdown_factory.create(
                    parent=self.frame,
                    variable=var,
                    values=files,
                    format=self.dropdowns[section_name]["format"]
                )
                self.config_dropdown.pack(fill="x", pady=5)

            else:
                self.selected_report = var
                self.report_dropdown = self.dropdown_factory.create(
                    parent=self.frame,
                    variable=var,
                    values=files,
                    format=self.dropdowns[section_name]["format"]
                )
                self.report_dropdown.pack(fill="x", pady=5)

        elif section_type == "button":
            self.button_factory.create(
                parent=self.frame,
                text=self.buttons["convert"],
                command=self.run_translation
            ).pack(pady=20)

        elif section_type == "status":
            self.progress = self.progress_factory.create(self.frame)
            self.status_factory = StatusLabelFactory(self.status_cfg)
            self.status_label   = self.status_factory.create(self.frame)


    def create_window(self):
        """Crea el canvas, el degradado, el frame y la barra de título."""
        # Barra personalizada
        TitleBar(
            parent     = self,
            app        = self,
            window_cfg = self.window_cfg,
            bar_cfg    = self.titlebar_cfg
        )

        # Canvas con degradado
        self.canvas = tk.Canvas(
            master             = self,
            width              = 1024,
            height             = 640,
            highlightthickness = 0
        )
        self.canvas.pack(fill="both", expand=True)
        self.draw_horizontal_gradient(
            canvas = self.canvas,
            color1 = self.window_cfg["gradient_start"],
            color2 = self.window_cfg["gradient_end"]
        )

        # Frame sobre el canvas
        size_str        = self.window_cfg["size"]
        width, height   = map(int, size_str.lower().split("x"))
        titlebar_height = self.titlebar_cfg["height"]

        self.frame = tk.Frame(
            master = self.canvas,
            padx   = self.frame_cfg["padx"],
            pady   = self.frame_cfg["pady"],
            width  = self.frame_cfg["width"],
            height = self.frame_cfg["height"],
            bg     = self.frame_cfg["bg_color"]
        )

        self.canvas.create_window(
            width // 2 + self.frame_cfg["offset_x"],
            (height - titlebar_height) // 2 + self.frame_cfg["offset_y"],
            window=self.frame,
            anchor=self.frame_cfg["anchor"]
        )
        

    def center_window(self):
        size_str = self.window_cfg["size"]
        width, height = map(int, size_str.lower().split("x"))

        # obtener tamaño de pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calcular coordenadas para centrar
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # aplicar geometría con posición
        self.geometry(f"{width}x{height}+{x}+{y}")

    def draw_horizontal_gradient(self, canvas, color1, color2):
        # Obtener tamaño desde el JSON (ejemplo: "1024x640")
        size_str = self.window_cfg["size"]
        width, height = map(int, size_str.lower().split("x"))

        # Convertir colores a RGB
        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)

        # Calcular ratios
        r_ratio = (r2 - r1) / width
        g_ratio = (g2 - g1) / width
        b_ratio = (b2 - b1) / width

        # Dibujar líneas verticales
        for x in range(width):
            nr = int(r1 + (r_ratio * x))
            ng = int(g1 + (g_ratio * x))
            nb = int(b1 + (b_ratio * x))
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            canvas.create_line(x, 0, x, height, fill=color)

    def get_files(self, folder, ext):
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        return [f for f in os.listdir(folder) if f.endswith(ext)]

    def run_translation(self):
        try:
            self.progress.pack(pady=10)

            # Recuperar valor real del config seleccionado
            config_real = DropdownFactory.get_real_value(self.selected_config, self.config_dropdown)
            config_path = os.path.join("config", config_real)
            if not os.path.exists(config_path):
                self.status_factory.show_error(self.status_label)
                return

            config = cp.load_config(config_path)
            reference = config[cp_cfg.student_list_key]
            classroom = fc.fetch_classroom_reference(reference=reference)

            # Recuperar valor real del reporte seleccionado
            report_real = DropdownFactory.get_real_value(self.selected_report, self.report_dropdown)
            report = os.path.join("reports", report_real)
            if not os.path.exists(report):
                self.status_factory.show_error(self.status_label)
                return

            self.progress["maximum"] = 1
            self.progress["value"] = 0

            total, kahoot = fc.fetch_kahoot_report(report=report)
            translation = tr.translate_kahoot_report(
                report=kahoot,
                total=total,
                reference=classroom
            )
            sv.save_report(report=report, reference=reference, data=translation)

            self.progress["value"] = 1
            self.update_idletasks()

            self.status_factory.show_success(self.status_label)

        except Exception as e:
            self.status_factory.show_error(self.status_label)
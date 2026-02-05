import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk

class LabelFactory:
    def __init__(self, config):
        self.font = tkfont.Font(family=config["font_family"], size=config["font_size"])
        self.bg_color = config["bg_color"]
        self.fg_color = config["fg_color"]

    def create(self, parent, text, **kwargs):
        return tk.Label(parent, text=text, font=self.font, bg=self.bg_color, fg=self.fg_color, relief="flat", **kwargs)

class DropdownFactory:
    def __init__(self, config):
        self.style_name  = "Custom.TMenubutton"
        self.font_family = config["font_family"]
        self.font_size   = config["font_size"]
        self.bg_color    = config["bg_color"]
        self.fg_color    = config["fg_color"]
        self.radius      = config["corner_radius"]
        self.max_chars   = config.get("max_chars", 20)
        self.fixed_width = config.get("fixed_width", 200)

        style = ttk.Style()
        style.configure(
            self.style_name,
            font=(self.font_family, self.font_size),
            relief="flat",
            borderwidth=0,
            padding=(self.radius, self.radius),
            background=self.bg_color,
            foreground=self.fg_color
        )

    def truncate(self, text):
        if len(text) > self.max_chars:
            return text[:self.max_chars - 3] + "..."
        return text

    def format_name(self, filename):
        """Quita extensión, reemplaza '_' por espacios y capitaliza."""
        return " ".join(
            word.capitalize() if i else f"{word.upper()}:"
            for i, word in enumerate(
                re.sub(r"\..*$", "", filename).replace("_", " ").split()
            )
        )

    def display_name(self, v, format: bool = False):
        return self.truncate(self.format_name(v) if format else v)

    def create(self, parent, variable, values, format: bool):
        """Crea un dropdown con valores reales y nombres formateados."""
        # Construir mapping {display -> real}
        mapping = {}
        for v in values:
            if not re.fullmatch(r"^template\.\w+$", v):
                display = self.display_name(v, format)
                mapping[display] = v

        # Valor inicial
        initial_real = variable.get() or (values[0] if values else "")
        initial_display = "Seleccione una opción"
        variable.set(initial_display)

        # Crear OptionMenu con claves formateadas
        menu = ttk.OptionMenu(parent, variable, initial_display, *mapping.keys())
        menu.configure(style=self.style_name, width=self.fixed_width // 10)

        # Reconfigurar menú interno
        menu["menu"].delete(0, "end")
        for display, real in mapping.items():
            menu["menu"].add_command(
                label=display,
                command=lambda val=display: variable.set(val)
            )

        # Guardar mapping en el widget para recuperar valor real
        menu._mapping = mapping
        return menu

    @staticmethod
    def get_real_value(variable, menu):
        """Helper para obtener el valor real desde el valor mostrado."""
        display = variable.get()
        return menu._mapping.get(display, display)
    
class ButtonFactory:
    def __init__(self, config):
        self.style_name = "Custom.TButton"
        style = ttk.Style()
        style.configure(
            self.style_name,
            font=(config["font_family"], config["font_size"]),
            background=config["bg_color"],
            foreground=config["fg_color"],
            relief="flat",
            borderwidth=0,
            padding=(config["corner_radius"], config["corner_radius"])
        )
        style.map(
            self.style_name,
            background=[("active", config["bg_color"])],
            foreground=[("active", config["fg_color"])]
        )

    def create(self, parent, text, command):
        return ttk.Button(parent, text=text, command=command, style=self.style_name)


class ProgressFactory:
    def __init__(self, config):
        self.style_name = "Custom.Horizontal.TProgressbar"
        style = ttk.Style()
        style.configure(
            self.style_name,
            troughcolor=config["trough_color"],
            background=config["bg_color"],
            relief="flat",
            borderwidth=0,
            padding=(config["corner_radius"], config["corner_radius"])
        )

    def create(self, parent, length=400):
        bar = ttk.Progressbar(parent, orient="horizontal", length=length,
                              mode="determinate", style=self.style_name)
        bar.pack_forget()
        return bar

class StatusLabelFactory:
    def __init__(self, config):
        self.font = tkfont.Font(family=config["font_family"], size=config["font_size"])
        self.fg_color = config["fg_color"]
        self.bg_color = config["bg_color"]
        self.success_text = config["success_text"]
        self.error_text = config["error_text"]

    def create(self, parent):
        label = tk.Label(
            parent,
            text="",
            font=self.font,
            fg=self.fg_color,
            bg=self.bg_color,
            relief="flat"
        )
        label.pack_forget()  # inicialmente oculto
        return label

    def show_success(self, label):
        label.config(text=self.success_text)
        label.pack(pady=10)

    def show_error(self, label):
        label.config(text=self.error_text)
        label.pack(pady=10)


class TitleBar(tk.Canvas):
    def __init__(self, parent, app, window_cfg, bar_cfg):
        size_str = window_cfg["size"]
        width, _ = map(int, size_str.lower().split("x"))
        height = bar_cfg["height"]

        super().__init__(parent, width=width, height=height, highlightthickness=0)
        self.app = app
        self.pack(fill="x")

        # Dibujar gradiente
        self.draw_horizontal_gradient(window_cfg["gradient_start"], window_cfg["gradient_end"], width, height)

        # Logo PNG transparente redimensionado
        if "logo_path" in bar_cfg and os.path.exists(bar_cfg["logo_path"]):
            img = Image.open(bar_cfg["logo_path"])
            ratio = bar_cfg["logo_height"] / img.height
            new_size = (int(img.width * ratio), bar_cfg["logo_height"])
            img = img.resize(new_size, Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            self.create_image(bar_cfg["logo_x"], bar_cfg["logo_y"], image=self.logo_img, anchor="w")

        # Botón cerrar
        close_x = width - bar_cfg["close_offset_x"]
        close_y = bar_cfg["close_offset_y"]
        close_color = self.gradient_color_at(close_x, window_cfg["gradient_start"], window_cfg["gradient_end"], width)

        close_btn = tk.Button(
            self,
            text=bar_cfg["close_text"],
            bg=close_color,
            fg=bar_cfg["fg_color"],
            font=(bar_cfg["close_font_family"], bar_cfg["close_font_size"]),
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=self.app.destroy
        )
        self.create_window(close_x, close_y, window=close_btn)

        # Arrastrar ventana
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

    def draw_horizontal_gradient(self, color1, color2, width, height):
        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)
        r_ratio = (r2 - r1) / width
        g_ratio = (g2 - g1) / width
        b_ratio = (b2 - b1) / width
        for x in range(width):
            nr = int(r1 + (r_ratio * x))
            ng = int(g1 + (g_ratio * x))
            nb = int(b1 + (b_ratio * x))
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            self.create_line(x, 0, x, height, fill=color)

    def gradient_color_at(self, x, color1, color2, width):
        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)
        r = int(r1 + (r2 - r1) * x / width)
        g = int(g1 + (g2 - g1) * x / width)
        b = int(b1 + (b2 - b1) * x / width)
        return f"#{r//256:02x}{g//256:02x}{b//256:02x}"

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.app.winfo_x() + deltax
        y = self.app.winfo_y() + deltay
        self.app.geometry(f"+{x}+{y}")
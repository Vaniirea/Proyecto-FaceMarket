import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random

# Paleta de colores y estilos
PRIMARY_COLOR = "#3F51B5"      # Azul índigo
ACCENT_COLOR = "#FF9800"       # Naranja
BG_COLOR = "#FAFAFA"           # Fondo claro
HEADER_FG = "#FFFFFF"          # Texto blanco
BUTTON_FG = "#FFFFFF"          # Texto blanco
ERROR_BG = "#F44336"           # Rojo para botones de advertencia

# Fuentes
HEADER_FONT = ("Helvetica", 26, "bold")
TITLE_FONT = ("Helvetica", 20, "bold")
LABEL_FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 16, "bold")
TEXT_FONT = ("Helvetica", 14)


class SelfCheckoutApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tienda de Autocobro")

        # Maximizar la ventana en Windows
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))


        # Variables compartidas
        self.cart = []  # Lista de productos (tuplas: (nombre, precio, cantidad))
        self.total = 0.0

        # Catálogo de productos (simulado)
        self.products = {
            "001": ("Manzana", 1.0),
            "002": ("Banana", 0.5),
            "003": ("Leche", 1.5),
            "004": ("Pan", 2.0)
        }

        # Contenedor para las páginas
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        # Diccionario para almacenar las páginas
        self.frames = {}
        for F in (ProductPage, PaymentPage, TicketPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ProductPage)

    def show_frame(self, page_class):
        """Muestra la página solicitada."""
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "update_page"):
            frame.update_page()

    def reset(self):
        """Reinicia el carrito y el total."""
        self.cart = []
        self.total = 0.0


class ProductPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        # Cabecera
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        header_label = tk.Label(
            header,
            text="Escanear Productos",
            font=HEADER_FONT,
            bg=PRIMARY_COLOR,
            fg=HEADER_FG
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Contenido principal
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Fila 0: botones superiores
        buttons_frame = tk.Frame(content, bg=BG_COLOR)
        buttons_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=5)

        self.scan_button = tk.Button(
            buttons_frame, text="Escanear Producto",
            font=BUTTON_FONT, bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=self.scan_product,
            relief=tk.RAISED, bd=3
        )
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))

        self.remove_button = tk.Button(
            buttons_frame, text="Eliminar Producto",
            font=BUTTON_FONT, bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=self.remove_product,
            relief=tk.RAISED, bd=3
        )
        self.remove_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = tk.Button(
            buttons_frame, text="Vaciar Carrito",
            font=BUTTON_FONT, bg=ERROR_BG, fg=BUTTON_FG,
            command=self.clear_cart,
            relief=tk.RAISED, bd=3
        )
        self.clear_button.pack(side=tk.LEFT)

        # Fila 1: Carrito de compras (LabelFrame)
        cart_frame = tk.LabelFrame(
            content,
            text="Carrito de Compras",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=PRIMARY_COLOR,
            padx=10, pady=10
        )
        cart_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        self.cart_listbox = tk.Listbox(
            cart_frame, font=TEXT_FONT, bd=2, relief=tk.GROOVE
        )
        self.cart_listbox.pack(fill=tk.BOTH, expand=True)

        # Fila 2: total (col 0) y botón siguiente (col 1)
        self.total_label = tk.Label(
            content, text="Total: $0.00",
            font=("Helvetica", 18, "bold"),
            bg=BG_COLOR
        )
        self.total_label.grid(row=2, column=0, pady=5, sticky="w")

        self.next_button = tk.Button(
            content, text="Siguiente",
            font=BUTTON_FONT,
            bg=PRIMARY_COLOR, fg=BUTTON_FG,
            command=lambda: controller.show_frame(PaymentPage),
            relief=tk.RAISED, bd=3
        )
        self.next_button.grid(row=2, column=1, pady=5, sticky="e")

        # Ajustar la expansión de filas/columnas
        content.grid_rowconfigure(1, weight=1)   # la fila del carrito se expande
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

    def scan_product(self):
        """Solicita el código y la cantidad del producto y actualiza el carrito."""
        code = simpledialog.askstring("Escanear Producto", "Ingrese el código del producto:")
        if code:
            code = code.strip()
            if code in self.controller.products:
                product, price = self.controller.products[code]
                qty = simpledialog.askinteger(
                    "Cantidad",
                    f"Ingrese la cantidad de {product}:",
                    minvalue=1, initialvalue=1
                )
                if not qty:
                    qty = 1
                self.controller.cart.append((product, price, qty))
                self.controller.total += price * qty
                self.cart_listbox.insert(tk.END, f"{product} x{qty} - ${price * qty:.2f}")
                self.total_label.config(text=f"Total: ${self.controller.total:.2f}")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")

    def remove_product(self):
        """Elimina el producto seleccionado del carrito."""
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            product, price, qty = self.controller.cart.pop(index)
            self.controller.total -= price * qty
            self.cart_listbox.delete(index)
            self.total_label.config(text=f"Total: ${self.controller.total:.2f}")
        else:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")

    def clear_cart(self):
        """Vacía todo el carrito después de confirmar."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de vaciar el carrito?"):
            self.controller.reset()
            self.update_page()

    def update_page(self):
        """Actualiza la página al volver a ella."""
        self.cart_listbox.delete(0, tk.END)
        self.total_label.config(text=f"Total: ${self.controller.total:.2f}")
        for product, price, qty in self.controller.cart:
            self.cart_listbox.insert(tk.END, f"{product} x{qty} - ${price * qty:.2f}")


class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        # Cabecera
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        header_label = tk.Label(
            header,
            text="Métodos de Pago",
            font=HEADER_FONT,
            bg=PRIMARY_COLOR,
            fg=HEADER_FG
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Contenido principal
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Fila 0: label con total a pagar
        self.total_label = tk.Label(content, text="", font=LABEL_FONT, bg=BG_COLOR)
        self.total_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")

        # Fila 1: Botones Face ID y Tarjeta
        self.faceid_button = tk.Button(
            content, text="Pago Face ID",
            font=BUTTON_FONT,
            bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=lambda: self.process_payment("Face ID"),
            relief=tk.RAISED, bd=3
        )
        self.faceid_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.card_button = tk.Button(
            content, text="Pago con Tarjeta",
            font=BUTTON_FONT,
            bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=lambda: self.process_payment("Tarjeta"),
            relief=tk.RAISED, bd=3
        )
        self.card_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Fila 2: Botón Pago con QR (ocupa 2 columnas)
        self.qr_button = tk.Button(
            content, text="Pago con QR",
            font=BUTTON_FONT,
            bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=lambda: self.process_payment("QR"),
            relief=tk.RAISED, bd=3
        )
        self.qr_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Fila 3: Botón Finalizar
        self.finalize_button = tk.Button(
            content, text="Finalizar Compra",
            font=BUTTON_FONT,
            bg=ERROR_BG, fg=BUTTON_FG,
            command=self.finalize_purchase,
            relief=tk.RAISED, bd=3
        )
        self.finalize_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Ajustar expansión
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=1)
        content.grid_rowconfigure(3, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

    def update_page(self):
        """Actualiza el total a pagar en la página de pago."""
        self.total_label.config(text=f"Total a pagar: ${self.controller.total:.2f}")

    def process_payment(self, method):
        """Simula el proceso de pago según el método seleccionado."""
        messagebox.showinfo(method, f"Iniciando pago con {method}...")
        self.after(2000, lambda: self.show_payment_result(method))

    def show_payment_result(self, method):
        # Simulación: mayor probabilidad de éxito
        success = random.choice([True, True, False])
        if success:
            messagebox.showinfo("Pago Exitoso", f"Pago con {method} aprobado.")
        else:
            messagebox.showwarning("Error", f"El pago con {method} falló. Intente nuevamente.")

    def finalize_purchase(self):
        """Finaliza la compra y pasa a la ventana del ticket."""
        if self.controller.total == 0:
            messagebox.showwarning("Carrito Vacío", "No hay productos en el carrito.")
        else:
            self.controller.show_frame(TicketPage)


class TicketPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        # Cabecera
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        header_label = tk.Label(
            header,
            text="Ticket de Compra",
            font=HEADER_FONT,
            bg=PRIMARY_COLOR,
            fg=HEADER_FG
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Contenido principal
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Fila 0: Área para mostrar el ticket (Text)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.ticket_text = tk.Text(
            content, font=TEXT_FONT, bg="white",
            bd=2, relief=tk.GROOVE, state=tk.DISABLED
        )
        self.ticket_text.grid(row=0, column=0, sticky="nsew")

        # Fila 1: Frame para botones (Guardar / Finalizar)
        buttons_frame = tk.Frame(content, bg=BG_COLOR)
        buttons_frame.grid(row=1, column=0, sticky="e", pady=5)

        self.save_button = tk.Button(
            buttons_frame, text="Guardar Ticket",
            font=BUTTON_FONT,
            bg=ACCENT_COLOR, fg=BUTTON_FG,
            command=self.save_ticket,
            relief=tk.RAISED, bd=3
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.finish_button = tk.Button(
            buttons_frame, text="Finalizar",
            font=BUTTON_FONT,
            bg=PRIMARY_COLOR, fg=BUTTON_FG,
            command=self.finish_purchase,
            relief=tk.RAISED, bd=3
        )
        self.finish_button.pack(side=tk.LEFT, padx=5)

    def update_page(self):
        """Genera y muestra el ticket con la información de la compra."""
        self.ticket_text.config(state=tk.NORMAL)
        self.ticket_text.delete("1.0", tk.END)
        self.ticket_text.insert(tk.END, "----- TICKET DE COMPRA -----\n\n")
        for product, price, qty in self.controller.cart:
            self.ticket_text.insert(tk.END, f"{product} x{qty}: ${price * qty:.2f}\n")
        self.ticket_text.insert(tk.END, f"\nTotal a pagar: ${self.controller.total:.2f}\n")
        self.ticket_text.insert(tk.END, "\n¡Gracias por su compra!")
        self.ticket_text.config(state=tk.DISABLED)

    def save_ticket(self):
        """Guarda el ticket en un archivo de texto."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.ticket_text.get("1.0", tk.END))
            messagebox.showinfo("Guardado", "El ticket ha sido guardado exitosamente.")

    def finish_purchase(self):
        """Reinicia la compra y vuelve a la página de escaneo de productos."""
        self.controller.reset()
        self.controller.show_frame(ProductPage)


if __name__ == "__main__":
    app = SelfCheckoutApp()
    app.mainloop()

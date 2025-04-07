[Volver al README](https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/README.md)

## Main.py
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random
import face_recognition
import cv2
import os
import numpy as np
import glob
import time
from conexion import obtener_conexion_gestion_usuario, obtener_conexion_productos

# Configuracion
RUTA_FACES = "faces"
PRIMARY_COLOR = "#3F51B5"
ACCENT_COLOR = "#FF9800"
BG_COLOR = "#FAFAFA"
HEADER_FG = "#FFFFFF"
BUTTON_FG = "#FFFFFF"
ERROR_BG = "#F44336"

HEADER_FONT = ("Helvetica", 26, "bold")
TITLE_FONT = ("Helvetica", 20, "bold")
LABEL_FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 16, "bold")
TEXT_FONT = ("Helvetica", 14)

clientes_rostros = {}
productos_db = {}

def precargar_rostros():
    for carpeta in os.listdir(RUTA_FACES):
        ruta = os.path.join(RUTA_FACES, carpeta)
        if os.path.isdir(ruta) and carpeta.isdigit():
            id_cliente = int(carpeta)
            encodings = []
            for archivo in glob.glob(os.path.join(ruta, "*.jpg")) + glob.glob(os.path.join(ruta, "*.jpeg")):
                img = face_recognition.load_image_file(archivo)
                cods = face_recognition.face_encodings(img)
                if cods:
                    encodings.append(cods[0])
            if encodings:
                clientes_rostros[id_cliente] = encodings

def precargar_productos():
    global productos_db
    productos_db.clear()
    try:
        conn = obtener_conexion_productos()
        cursor = conn.cursor()
        cursor.execute("SELECT Codigo, Nombre, Precio FROM Productos")
        for fila in cursor.fetchall():
            productos_db[fila.Codigo] = (fila.Nombre, float(fila.Precio))
        conn.close()
    except Exception as e:
        print("Error al cargar productos:", e)

def identificar_cliente_por_rostro():
    cam = cv2.VideoCapture(0)
    print("Verificando rostro...")
    for _ in range(3):
        time.sleep(1)
        ret, frame = cam.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb)
        codificaciones = face_recognition.face_encodings(rgb, ubicaciones)
        for cod_actual in codificaciones:
            for id_cliente, lista_encodings in clientes_rostros.items():
                distancias = face_recognition.face_distance(lista_encodings, cod_actual)
                if distancias.size > 0 and np.min(distancias) < 0.6:
                    cam.release()
                    cv2.destroyAllWindows()
                    return id_cliente
        cv2.imshow("Verificando...", frame)
        if cv2.waitKey(2000) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    return None

class ProductPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="Escanear Productos", font=HEADER_FONT,
                 bg=PRIMARY_COLOR, fg=HEADER_FG).pack(side=tk.LEFT, padx=20, pady=10)
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        buttons_frame = tk.Frame(content, bg=BG_COLOR)
        buttons_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")
        tk.Button(buttons_frame, text="Escanear Producto", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=self.scan_product).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(buttons_frame, text="Eliminar Producto", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=self.remove_product).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(buttons_frame, text="Vaciar Carrito", font=BUTTON_FONT,
                  bg=ERROR_BG, fg=BUTTON_FG, command=self.clear_cart).pack(side=tk.LEFT)
        cart_frame = tk.LabelFrame(content, text="Carrito de Compras", font=TITLE_FONT,
                                   bg=BG_COLOR, fg=PRIMARY_COLOR, padx=10, pady=10)
        cart_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
        self.cart_listbox = tk.Listbox(cart_frame, font=TEXT_FONT)
        self.cart_listbox.pack(fill=tk.BOTH, expand=True)
        self.total_label = tk.Label(content, text="Total: $0.00", font=("Helvetica", 18, "bold"), bg=BG_COLOR)
        self.total_label.grid(row=2, column=0, pady=5, sticky="w")
        tk.Button(content, text="Siguiente", font=BUTTON_FONT,
                  bg=PRIMARY_COLOR, fg=BUTTON_FG, command=lambda: controller.show_frame(PaymentPage)).grid(row=2, column=1, pady=5, sticky="e")
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

    def scan_product(self):
        code = simpledialog.askstring("Código del producto", "Ingrese el código:")
        if code:
            code = code.strip()
            if code in productos_db:
                name, price = productos_db[code]
                qty = simpledialog.askinteger("Cantidad", f"¿Cuántos {name}?", minvalue=1, initialvalue=1)
                if not qty:
                    return
                self.controller.cart.append((name, price, qty))
                self.controller.total += price * qty
                self.cart_listbox.insert(tk.END, f"{name} x{qty} - ${price * qty:.2f}")
                self.total_label.config(text=f"Total: ${self.controller.total:.2f}")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")

    def remove_product(self):
        idx = self.cart_listbox.curselection()
        if idx:
            item = self.controller.cart.pop(idx[0])
            self.controller.total -= item[1] * item[2]
            self.cart_listbox.delete(idx)
            self.total_label.config(text=f"Total: ${self.controller.total:.2f}")

    def clear_cart(self):
        if messagebox.askyesno("Confirmar", "¿Vaciar carrito?"):
            self.controller.reset()
            self.update_page()

    def update_page(self):
        self.cart_listbox.delete(0, tk.END)
        self.total_label.config(text=f"Total: ${self.controller.total:.2f}")
        for name, price, qty in self.controller.cart:
            self.cart_listbox.insert(tk.END, f"{name} x{qty} - ${price * qty:.2f}")

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="Métodos de Pago", font=HEADER_FONT,
                 bg=PRIMARY_COLOR, fg=HEADER_FG).pack(side=tk.LEFT, padx=20, pady=10)
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.total_label = tk.Label(content, text="", font=LABEL_FONT, bg=BG_COLOR)
        self.total_label.grid(row=0, column=0, columnspan=2, pady=5)
        tk.Button(content, text="Pago Face ID", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=self.pago_con_faceid).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(content, text="Pago con Tarjeta", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=lambda: self.simular_pago("Tarjeta")).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(content, text="Pago con QR", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=lambda: self.simular_pago("QR")).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        tk.Button(content, text="Finalizar Compra", font=BUTTON_FONT,
                  bg=ERROR_BG, fg=BUTTON_FG, command=self.finalizar).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        for i in range(4):
            content.grid_rowconfigure(i, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

    def update_page(self):
        self.total_label.config(text=f"Total a pagar: ${self.controller.total:.2f}")

    def pago_con_faceid(self):
        id_cliente = identificar_cliente_por_rostro()
        if id_cliente is None:
            messagebox.showwarning("Error", "No se pudo verificar tu identidad.")
            return
        try:
            conexion = obtener_conexion_gestion_usuario()
            cursor = conexion.cursor()
            cursor.execute("SELECT Saldo FROM Clientes WHERE IdCliente = ?", (id_cliente,))
            fila = cursor.fetchone()
            if not fila:
                messagebox.showerror("Error", "Cliente no encontrado en base de datos.")
                return
            saldo_actual = float(fila.Saldo)
            if saldo_actual >= self.controller.total:
                nuevo_saldo = saldo_actual - self.controller.total
                cursor.execute("UPDATE Clientes SET Saldo = ? WHERE IdCliente = ?", (nuevo_saldo, id_cliente))
                conexion.commit()
                messagebox.showinfo("Pago Exitoso", f"Pago aprobado. Nuevo saldo: ${nuevo_saldo:.2f}")
                self.controller.show_frame(TicketPage)
            else:
                messagebox.showerror("Saldo insuficiente", "No tienes suficiente saldo para completar la compra.")
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))

    def simular_pago(self, metodo):
        messagebox.showinfo(metodo, f"Procesando pago con {metodo}...")
        self.after(2000, lambda: messagebox.showinfo("Éxito", f"Pago con {metodo} aprobado."))

    def finalizar(self):
        if self.controller.total == 0:
            messagebox.showwarning("Carrito Vacío", "No hay productos en el carrito.")
        else:
            self.controller.show_frame(TicketPage)

class TicketPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        header = tk.Frame(self, bg=PRIMARY_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="Ticket de Compra", font=HEADER_FONT,
                 bg=PRIMARY_COLOR, fg=HEADER_FG).pack(side=tk.LEFT, padx=20, pady=10)
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.ticket_text = tk.Text(content, font=TEXT_FONT, bg="white", state=tk.DISABLED)
        self.ticket_text.pack(fill=tk.BOTH, expand=True)
        buttons_frame = tk.Frame(content, bg=BG_COLOR)
        buttons_frame.pack(anchor="e", pady=5)
        tk.Button(buttons_frame, text="Guardar Ticket", font=BUTTON_FONT,
                  bg=ACCENT_COLOR, fg=BUTTON_FG, command=self.save_ticket).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Finalizar", font=BUTTON_FONT,
                  bg=PRIMARY_COLOR, fg=BUTTON_FG, command=self.finish_purchase).pack(side=tk.LEFT, padx=5)

    def update_page(self):
        self.ticket_text.config(state=tk.NORMAL)
        self.ticket_text.delete("1.0", tk.END)
        self.ticket_text.insert(tk.END, "----- TICKET DE COMPRA -----\n\n")
        for product, price, qty in self.controller.cart:
            self.ticket_text.insert(tk.END, f"{product} x{qty}: ${price * qty:.2f}\n")
        self.ticket_text.insert(tk.END, f"\nTotal a pagar: ${self.controller.total:.2f}\n")
        self.ticket_text.insert(tk.END, "\n\n¡Gracias por su compra!")
        self.ticket_text.config(state=tk.DISABLED)

    def save_ticket(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.ticket_text.get("1.0", tk.END))
            messagebox.showinfo("Guardado", "Ticket guardado exitosamente.")

    def finish_purchase(self):
        self.controller.reset()
        self.controller.show_frame(ProductPage)

class SelfCheckoutApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tienda de Autocobro")
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.cart = []
        self.total = 0.0
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (ProductPage, PaymentPage, TicketPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ProductPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "update_page"):
            frame.update_page()

    def reset(self):
        self.cart = []
        self.total = 0.0

if __name__ == "__main__":
    precargar_rostros()
    precargar_productos()
    app = SelfCheckoutApp()
    app.mainloop()

## Diseño.py
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

## Cara.py
import cv2
import face_recognition
import numpy as np
import os


def register_face(customer_name: str):
    """ Captura y guarda la cara del cliente con su nombre. """
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al acceder a la cámara")
            break

        cv2.imshow("Registrar Rostro - Presiona 's' para guardar", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Guardar la imagen en la carpeta "faces"
            os.makedirs("faces", exist_ok=True)
            image_path = os.path.join("faces", f"{customer_name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Rostro guardado en: {image_path}")
            break
        elif key == ord('q'):
            print("Registro cancelado.")
            break

    cam.release()
    cv2.destroyAllWindows()


def authenticate_face_real():
    """ Escanea el rostro y lo compara con los registros existentes. """
    known_faces = {}
    faces_dir = "faces"

    if not os.path.exists(faces_dir):
        print("No hay rostros registrados.")
        return False

    # Cargar rostros almacenados
    for filename in os.listdir(faces_dir):
        if filename.endswith(".jpg"):
            img_path = os.path.join(faces_dir, filename)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_faces[filename.split(".")[0]] = encodings[0]

    if not known_faces:
        print("No se encontraron rostros válidos en la base de datos.")
        return False

    cam = cv2.VideoCapture(0)
    print("Escaneando rostro...")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error con la cámara.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            face_distances = face_recognition.face_distance(list(known_faces.values()), face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = list(known_faces.keys())[best_match_index]
                print(f"Autenticación exitosa: {name}")
                cam.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Autenticando...", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Autenticación cancelada.")
            break

    cam.release()
    cv2.destroyAllWindows()
    print("No se encontró coincidencia.")
    return False

## Conexion.py
import pyodbc

def obtener_conexion_gestion_usuario():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=FM_Clientes;'
        'Trusted_Connection=yes;'
    )
    return conn

def obtener_conexion_productos():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=FM_Productos;'
        'Trusted_Connection=yes;'
    )
    return conn

## Prueba.py
import cv2
import face_recognition
import os
import pickle

# Configuración
nombre_persona = "Usuario1"
ruta_carpeta = f"faces/{nombre_persona}"
os.makedirs(ruta_carpeta, exist_ok=True)
num_imagenes = 100

# Capturar imágenes
cam = cv2.VideoCapture(0)
contador = 0

print(f"Capturando {num_imagenes} imágenes. Muévete lentamente para variar ángulos. Presiona 'q' para salir antes.")

while contador < num_imagenes:
    ret, frame = cam.read()
    if not ret:
        print("Error con la cámara.")
        break

    cv2.imshow("Captura - Mueve tu rostro", frame)

    # Guardar imagen cada frame
    ruta_imagen = os.path.join(ruta_carpeta, f"{nombre_persona}_{contador}.jpg")
    cv2.imwrite(ruta_imagen, frame)
    contador += 1
    print(f"Guardada imagen {contador}/{num_imagenes}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

# Generar encodings de las imágenes capturadas
encodings = []
for i in range(contador):
    ruta_imagen = os.path.join(ruta_carpeta, f"{nombre_persona}_{i}.jpg")
    imagen = face_recognition.load_image_file(ruta_imagen)
    encoding = face_recognition.face_encodings(imagen)
    if encoding:  # Solo si se detecta un rostro
        encodings.append(encoding[0])

# Guardar encodings en un archivo
if encodings:
    with open(f"faces/{nombre_persona}_encodings.pkl", "wb") as f:
        pickle.dump(encodings, f)
    print(f"Guardados {len(encodings)} encodings para {nombre_persona}.")
else:
    print("No se generaron encodings válidos.")

## Prueba por foto.py
import face_recognition
import cv2
import os
import numpy as np
import glob
import time

# Ruta a las imágenes registradas
RUTA_CARPETA = r'faces\vani'

def cargar_rostros(carpeta):
    """Carga y codifica todas las imágenes del cliente"""
    rostros_codificados = []
    for archivo in glob.glob(os.path.join(carpeta, "*.jpg")) + glob.glob(os.path.join(carpeta, "*.jpeg")):
        imagen = face_recognition.load_image_file(archivo)
        codificaciones = face_recognition.face_encodings(imagen)
        if codificaciones:
            rostros_codificados.append(codificaciones[0])
        else:
            print(f"[!] No se detectó rostro en: {archivo}")
    return rostros_codificados

def verificar_en_vivo(rostros_registrados, intentos=3):
    """Captura el rostro en vivo y lo compara contra los registrados (hasta 3 intentos)"""
    cam = cv2.VideoCapture(0)
    coincidencias = 0

    print(f"📷 Iniciando verificación facial. Tienes {intentos} intentos.\nPresiona 'q' para salir en cualquier momento.")

    for intento in range(intentos):
        print(f"\n🔍 Intento {intento + 1} de {intentos}...")

        time.sleep(1)  # Pequeña pausa entre intentos

        ret, frame = cam.read()
        if not ret:
            print("[!] Error con la cámara")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb)
        codificaciones = face_recognition.face_encodings(rgb, ubicaciones)

        encontrado = False
        for encoding in codificaciones:
            distancias = face_recognition.face_distance(rostros_registrados, encoding)
            mejor_distancia = np.min(distancias) if distancias.size > 0 else None

            if mejor_distancia is not None and mejor_distancia < 0.6:
                print(f"✅ Coincidencia detectada (distancia: {mejor_distancia:.2f})")
                coincidencias += 1
                encontrado = True
                break

        if not encontrado:
            print("❌ No se detectó coincidencia en este intento.")

        # Mostrar frame
        cv2.imshow("Verificación Facial", frame)
        if cv2.waitKey(2000) & 0xFF == ord('q'):  # Mostrar cada intento 2 segundos
            break

    cam.release()
    cv2.destroyAllWindows()

    # Resultado final
    print("\n🧾 Resultado final:")
    if coincidencias >= 1:
        print(f"✅ Verificación aprobada con {coincidencias} coincidencia(s).")
    else:
        print("❌ Verificación fallida. No se detectaron coincidencias.")

    return coincidencias >= 1


if __name__ == "__main__":
    rostros = cargar_rostros(RUTA_CARPETA)
    if not rostros:
        print("⚠️ No se pudieron cargar rostros desde la carpeta.")
    else:
        verificar_en_vivo(rostros)

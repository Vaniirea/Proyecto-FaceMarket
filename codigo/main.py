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

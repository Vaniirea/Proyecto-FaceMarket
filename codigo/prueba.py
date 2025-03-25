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
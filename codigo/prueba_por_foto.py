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

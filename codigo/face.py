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

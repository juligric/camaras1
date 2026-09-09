"""Detecta camaras conectadas y muestra el formato real de cada una.

Uso:  python detectar.py
"""
import cv2

BACKENDS = [
    ("DSHOW", cv2.CAP_DSHOW),
    ("MSMF", cv2.CAP_MSMF),
]


def fourcc_str(valor):
    n = int(valor)
    return "".join(chr((n >> (8 * i)) & 0xFF) for i in range(4))


def probar(indice, nombre_backend, backend):
    cap = cv2.VideoCapture(indice, backend)
    if not cap.isOpened():
        cap.release()
        return None

    # Sin conversion a RGB: asi vemos el formato crudo que entrega el sensor.
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
    ok, frame = cap.read()
    crudo = frame.shape if ok else None

    cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
    ok2, frame2 = cap.read()
    convertido = frame2.shape if ok2 else None

    info = {
        "indice": indice,
        "backend": nombre_backend,
        "ancho": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "alto": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "fourcc": fourcc_str(cap.get(cv2.CAP_PROP_FOURCC)),
        "shape_crudo": crudo,
        "shape_convertido": convertido,
    }
    cap.release()
    return info


def main():
    encontradas = []
    for indice in range(8):
        for nombre, backend in BACKENDS:
            info = probar(indice, nombre, backend)
            if info:
                encontradas.append(info)

    if not encontradas:
        print("No se detecto ninguna camara.")
        return

    for c in encontradas:
        print(f"--- indice {c['indice']} via {c['backend']}")
        print(f"    resolucion : {c['ancho']}x{c['alto']}  @ {c['fps']:.0f} fps")
        print(f"    fourcc     : {c['fourcc']}")
        print(f"    frame crudo (CONVERT_RGB=0) : {c['shape_crudo']}")
        print(f"    frame normal (CONVERT_RGB=1): {c['shape_convertido']}")

        alto = c["alto"]
        ancho = c["ancho"]
        if alto == 2 * 192 and ancho == 256:
            print("    >> Sensor termico 256x192 con dos mitades:")
            print("       arriba = imagen visible, abajo = datos de temperatura 16 bits")
        elif (ancho, alto) in {(256, 192), (240, 180), (384, 288), (640, 512)}:
            print("    >> Resolucion tipica de sensor termico")
        print()


if __name__ == "__main__":
    main()

"""Vigila la aparicion/desaparicion de dispositivos USB en tiempo real.

Deja esto corriendo y desconecta / vuelve a conectar la camara termica.
Si sale algo => Windows si la ve (problema de driver/formato).
Si no sale nada => el PC no la enumera (cable, puerto o camara solo-Android).

Salir con Ctrl+C.
"""
import subprocess
import time

PS = [
    "powershell.exe", "-NoProfile", "-Command",
    "Get-CimInstance Win32_PnPEntity | "
    "Where-Object { $_.PNPDeviceID -like 'USB*' } | "
    "ForEach-Object { $_.PNPDeviceID + ' | ' + $_.Name }",
]


def snapshot():
    out = subprocess.run(PS, capture_output=True, text=True).stdout
    return set(line.strip() for line in out.splitlines() if line.strip())


def main():
    print("Vigilando USB. Conecta/desconecta la camara termica ahora...")
    print("(Ctrl+C para salir)\n")
    anterior = snapshot()
    print(f"{len(anterior)} dispositivos USB al inicio.\n")
    try:
        while True:
            time.sleep(1)
            actual = snapshot()
            for d in actual - anterior:
                print(f"[+] CONECTADO : {d}")
            for d in anterior - actual:
                print(f"[-] QUITADO   : {d}")
            anterior = actual
    except KeyboardInterrupt:
        print("\nFin.")


if __name__ == "__main__":
    main()

import qrcode
import sys

# Pega o código do item dos argumentos ou usa um padrão
codigo = sys.argv[1] if len(sys.argv) > 1 else "TC.000.296"

print(f"\nGerando QR Code para: {codigo}\n")

qr = qrcode.QRCode()
qr.add_data(codigo)
qr.make()

qr.print_ascii(invert=True)
print("\n")

import numpy
import cv2
import qrcode
import os

class QR_CODE:

    def __init__(self):
        self.ruta = 'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/QR/'

    def crear_nuevo_qr(self, producto: str, link: str, user: str) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make()
        img = qr.make_image()

        rutaUser = self.ruta + user + '/'

        if not os.path.exists(rutaUser):
            os.makedirs(rutaUser)

        img.save(rutaUser + producto + '.png')

    def leer_codigo(self, imagen: str) -> str:
        img = cv2.imread(self.ruta+imagen)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        det = cv2.QRCodeDetector()
        val, pts, st_code = det.detectAndDecode(img)

        return val


#a = QR_CODE()

#imagen = a.crear_nuevo_qr('hola', "http://127.0.0.1:8000/main/factura", 'angel')

#print(a.leer_codigo('hola.png'))
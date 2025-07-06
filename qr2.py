import qrcode
import cv2
import numpy as np

# Générer le QR code
data = "https://gykhamine.github.io/GCI/1.html"
qr = qrcode.make(data)

# Convertir en tableau NumPy puis en image affichable par OpenCV
qr_np = np.array(qr, dtype=np.uint8) * 255  # convert bool → uint8 (0 ou 255)

# Afficher avec OpenCV
cv2.imshow("QR Code", qr_np)
cv2.waitKey(10000)
cv2.destroyAllWindows()



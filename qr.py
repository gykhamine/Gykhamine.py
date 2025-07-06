import qrcode
from PIL import Image

# Texte ou lien à encoder
data = "https://www.openai.com"

# Génération simple du QR code
img = qrcode.make(data)

# Affichage à l'écran
img.show()

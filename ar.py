import qrcode

# Le texte ou le lien que vous voulez encoder
data = "https://www.openai.com"

# Créer un objet QRCode
qr = qrcode.QRCode(
    version=1,  # contrôle la taille du QR code (1 à 40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # niveau de correction d'erreur
    box_size=10,  # taille de chaque carré du QR code
    border=4,  # taille de la bordure (en carré)
)

# Ajouter les données
qr.add_data(data)
qr.make(fit=True)

# Créer une image du QR code
img = qr.make_image(fill_color="black", back_color="white")

# Sauvegarder l'image
img.save("qr_code.png")

print("QR code généré et sauvegardé sous 'qr_code.png'")

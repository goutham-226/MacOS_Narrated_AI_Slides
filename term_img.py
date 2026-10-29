from term_image.image import AutoImage
#from term_image.tty import set_tty
from term_image.image import from_file
#set_tty()  # Optional but helps in some terminals
img = AutoImage.from_file("out.jpg")
print(img)


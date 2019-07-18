from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pynput import keyboard

for i in range(65, 122):
    img = Image.open("Template.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Times_New_Roman.ttf", 30)
    draw.text((60, 55), chr(i),(0, 0, 0),font=font)
    img.save('{}.png'.format(chr(i)))
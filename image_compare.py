
from PIL import Image
from PIL import ImageChops

def compare(file1, file2):

   image_one = Image.open(file1).convert('RGB')
   image_two = Image.open(file2).convert('RGB')

   diff = ImageChops.difference(image_one, image_two)

   if diff.getbbox():
      return False
      
   else:
      return True
import face_recognition
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import face_recognition
import PIL.Image
import PIL.ImageOps
import numpy as np

known_face_names = ['']
face_encoding=[]
known_face_encodings=[]
direc=''

def exif_transpose(img):
    if not img:
        return img

    exif_orientation_tag = 274

    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotated 180 degrees
            img = img.rotate(180)
        elif orientation == 4:
            # Mirrored top to bottom
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # Rotated 90 degrees
            img = img.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # Rotated 270 degrees
            img = img.rotate(90, expand=True)

    return img


def load_image_file(file, mode='RGB'):
    # Load the image with PIL
    img = PIL.Image.open(file)

    if hasattr(PIL.ImageOps, 'exif_transpose'):
        # Very recent versions of PIL can do exit transpose internally
        img = PIL.ImageOps.exif_transpose(img)
    else:
        # Otherwise, do the exif transpose ourselves
        img = exif_transpose(img)

    img = img.convert(mode)

    return np.array(img)

def class1_init():
    global known_face_names, face_encoding, known_face_encodings

    known_face_names = ['juwon', 'seonho', 'yuchan', 'taeyoungK', 'taeyoungY', 'damhyun', 'hanjin', 'wonyoung',
                        'youngbin', 'chanmo', 'yerim', 'donghwa', 'sungbin']
    face_encoding = []
    known_face_encodings = [[] for i in range(0,13)]
    index1=0


    for i in range(0, 13):
        # image = face_recognition.load_image_file(direc+'known/'+known_face_names[i]+'_001.jpg')
        image = load_image_file(direc + 'known/' + known_face_names[i] + '_001.jpg')
        try:
            face_encoding.append(face_recognition.face_encodings(image)[0])
        except:
            plt.imshow(image, aspect='auto')
        known_face_encodings.append(face_encoding[i])
    print(known_face_encodings)



def class2_init():
    global known_face_names, face_encoding, known_face_encodings

    known_face_names = ['wooseok', 'seongho', 'beomjun', 'sanghoon', 'jinsoo', 'minjun', 'minsu', 'donggun', 'seokjun',
                        'sieun', 'huiwoo', 'jinuk']
    face_encoding = []
    known_face_encodings = [[] for i in range(0,12)]

    for i in range(0, 12):
        # image = face_recognition.load_image_file(direc+'known/'+known_face_names[i]+'_001.jpg')
        image = load_image_file(direc + 'known/' + known_face_names[i] + '_001.jpg')
        try:
            face_encoding.append(face_recognition.face_encodings(image)[0])
        except:
            plt.imshow(image, aspect='auto')
        known_face_encodings.append(face_encoding[i])
    print(known_face_encodings)


if __name__=="__main__":
    class1_init()
    class2_init()


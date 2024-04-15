import base64
from io import BytesIO
from PIL import Image


def img2base64(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    return base64.b64encode(byte_data)


def base642img(base64str):
    im_bytes = base64.b64decode(base64str)
    return Image.open(BytesIO(im_bytes))


def is_num(s):
    s = str(s)
    if s.count('.') == 1:
        left = s.split('.')[0]
        right = s.split('.')[1]
        if right.isdigit():
            if left.count('-') == 1 and left.startswith('-'):
                num = left.split['-'][-1]
                if num.isdigit():
                    return True
            elif left.isdigit():
                return True
    return False

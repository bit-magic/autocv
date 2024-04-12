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

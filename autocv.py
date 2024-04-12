import pyautogui
from flask import Flask
from utils import img2base64
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/screen*": {"origins": "*"}})

app = Flask(__name__)


@app.route('/screen', methods=['GET'])
@cross_origin()
def ocr():
    im = pyautogui.screenshot()
    return img2base64(im)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

import pyautogui
from flask import Flask, request
from utils import img2base64
from inter import eval
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/screen*": {"origins": "*"},
                            r"/inter*": {"origins": "*"}})

app = Flask(__name__)


@app.route('/screen', methods=['GET'])
@cross_origin()
def ocr():
    im = pyautogui.screenshot()
    return img2base64(im)


@app.route('/inter', methods=['POST'])
@cross_origin()
def inte():
    expr = request.json.get('expr')
    if isinstance(expr, list):
        return eval(lines=expr)
    return eval(expr)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

from flask import Flask, jsonify, request, url_for
from flask_cors import CORS, cross_origin
import torchvision.transforms as transforms
from PIL import Image
import os
import detect

UPLOAD_FOLDER = './uploads' #'C:/Users/derek/OneDrive/Desktop/Files/AntsNet_API/uploads'

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'1a1a1a1a1a1a1a1a1a'

# def transform_image(image_bytes):
#     scale = transforms.Compose([transforms.Resize(832)])
#     image = Image.open(io.BytesIO(image_bytes))
#     return scale(image).unsqeeze(0)

# def localize(image_bytes):
#     input = transform_image(image_bytes)
#     #predicted_class = detect(--weights runs/train/yolov5s_results/weights/best.pt --img 832 --conf 0.4 --source ../test/images)
#     return None #predicted_class

@app.route('/')
def hello():
    return 'hello world'

@app.route('/infer', methods=['GET', 'POST'])
@cross_origin()
def infer():
    if request.method == 'POST':
        img = request.files['file']
        filename = img.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(filepath)
        #img_bytes = img.read()
        #pred_class = localize(image_bytes)
        save_dir = detect.run(weights='best.pt', source=filepath, imgsz=832)
        #return '<img src='+ url_for('static', filename=f'{save_dir}/{filename}') +'>'
        #jsonify({'animal': 'mlem', 'something': 'nothing'})
        return jsonify({'inference_img': url_for('static', filename=f'{save_dir}/{filename}')})
    return '''
    <!doctype html>
    <title>AntsNet Image Processor</title>
    <h1>AntsNet Image Processor</h1>
    <h2>Upload an image to count ants</h2>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>

    '''
from _curses import flash
from flask import Flask, request, redirect, url_for, jsonify
import io
import os
from werkzeug.utils import secure_filename
from google.cloud import vision
from google.cloud.vision import types






app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=[ 'GET','POST'])
def upload_file():
    basedir = os.path.abspath(os.path.dirname(__file__))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))
        
            var= myImageVision(file.filename)
            ##return redirect(url_for('static',
            ##                        filename=filename,message=(jsonify(message=var), 200)))
            return jsonify(Anger=var[0],Joy=var[1],Surprise=var[2]), 200





    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''



def myImageVision (Filename)  :

    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        Filename)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs face detection on the image file
    response = client.face_detection(image=image)
    faces= response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    for face in faces:
        anger=(' {}'.format(likelihood_name[face.anger_likelihood]))
        joy=(' {}'.format(likelihood_name[face.joy_likelihood]))
        surprise=(' {}'.format(likelihood_name[face.surprise_likelihood]))

    return anger,joy,surprise

if __name__ == '__main__':
    app.run()
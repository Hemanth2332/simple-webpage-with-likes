import os, uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, Image 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    # if request.method != "Post":
    #     return render_template("404.html")
    
    if 'file' not in request.files:
        return redirect(url_for("4040.html"))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_image = Image(filename=filename)
        db.session.add(new_image)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/like/<int:image_id>')
def like(image_id):
    image = Image.query.get(image_id)
    if image:
        image.likes += 1
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run()

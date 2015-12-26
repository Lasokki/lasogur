import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from id_handler import id_handler

UPLOAD_FOLDER = 'var/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

id_handler = id_handler(6)

# Will be changed to something smarter when database is used
pic_count = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/<user>", methods=['GET', 'POST'])
@app.route('/', methods=['GET','POST'])
def upload_file(user=None):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            
            # Will be changed to something smarter when database is used
            global pic_count

            # Format: aaaaaa.jpg
            filename = id_handler.encode_id(pic_count + 1) + "." + file.filename.rsplit('.', 1)[1]

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            pic_count = pic_count + 1

            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template("index.html", user=user)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/gallery/<file_id>')
@app.route('/gallery')
def gallery(file_id=None):
    imgs = os.listdir(UPLOAD_FOLDER)
    
    gallery_links = map((lambda x: "/gallery/" + x.rsplit('.', 1)[0]), imgs)
    uploads_links = map((lambda x: "/uploads/" + x), imgs)

    paths = zip(gallery_links, uploads_links)

    file_path = None
    if file_id:

        for s in os.listdir(UPLOAD_FOLDER):
            if s.startswith(file_id):
                file_path = "/uploads/" + s
                break

    return render_template("gallery.html", paths=paths, file_path=file_path)

if __name__ == "__main__":
    app.run(debug=True)

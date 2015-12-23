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

@app.route('/gallery')
def gallery():
    imgs = os.listdir(UPLOAD_FOLDER)
    
    imgs = map((lambda x: "/uploads/" + x), imgs)
        
    return render_template("gallery.html", imgs=imgs)

if __name__ == "__main__":
    app.run(debug=True)

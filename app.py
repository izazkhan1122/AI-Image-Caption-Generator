from flask import Flask, render_template, request
from caption_generator import generate_caption
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part in the request"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Generate caption from your existing function
        caption = generate_caption(filepath)

        return render_template('index.html', caption=caption, image_url=filepath)

    # For GET request, just render the page without caption
    return render_template('index.html', caption=None, image_url=None)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


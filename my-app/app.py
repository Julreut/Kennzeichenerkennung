from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['EXAMPLES_FOLDER'] = 'static/examples/'
app.secret_key = 'your_secret_key'

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'mp4', 'avi'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    model_choice = request.form.get('model')
    example_choice = request.form.get('example')

    if not model_choice:
        flash('Please choose a model.', 'danger')
        return redirect(url_for('index'))

    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_url = url_for('static', filename=f'uploads/{filename}')
    elif example_choice:
        filename = example_choice
        file_path = os.path.join(app.config['EXAMPLES_FOLDER'], filename)
        file_url = url_for('static', filename=f'examples/{filename}')
    else:
        flash('Please upload a file or choose an example.', 'danger')
        return redirect(url_for('index'))

    # Mock inference result
    if model_choice == 'model1':
        output_text = "Mock Inference Result: Detected objects (YOLO Placeholder)"
        country = "Unbekannt"
    elif model_choice == 'model2':
        output_text = "Mock Inference Result: Detected license plate (ANPR Placeholder)"
        # Beispiel: Angenommen, die Inferenz ergibt ein Herkunftsland
        country = "Deutschland"  # Hardcoded oder durch Erkennung ersetzt
    else:
        flash('Invalid model choice.', 'danger')
        return redirect(url_for('index'))

    # Flash message for the model choice
    flash(f'Model chosen: {model_choice}. Inference completed.', 'success')
    return render_template(
        'result.html',
        file_url=file_url,
        filename=filename,
        output_text=output_text,
        country=country
    )

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXAMPLES_FOLDER'], exist_ok=True)
    app.run(debug=True)

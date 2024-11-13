from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

# Load the trained model
model_path = '/Users/tharun/Downloads/PROJECTS/New/NEW INVENTORY/ML Main/File/lung_disease_model.keras'
model = load_model(model_path)

# Initialize Flask app with explicit template path
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Class labels
class_labels = ['Bacterial Pneumonia', 'Corona Virus Disease', 'Normal', 'Tuberculosis', 'Viral Pneumonia']

# Function to preprocess the image
def prepare_image(file_path):
    img = load_img(file_path, target_size=(150, 150))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Rescale the image
    return img

# Define the main route
@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Save the uploaded file to the uploads directory
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Prepare the image and make a prediction
            img = prepare_image(file_path)
            predictions = model.predict(img)
            prediction_class = np.argmax(predictions)
            result = class_labels[prediction_class]

            # Generate URL for the uploaded image to be shown in the template
            image_url = url_for('static', filename='uploads/' + file.filename)
            return render_template("index.html", prediction=result, image_url=image_url)

    return render_template("index.html", prediction="", image_url=None)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

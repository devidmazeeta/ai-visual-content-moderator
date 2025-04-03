from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from PIL import Image
import os
import mysql.connector

# Azure SDK imports
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
db_config = {
    'host': 'localhost',
    'port': '8111',
    'user': 'root',
    'password': '',  # your MySQL password
    'database': 'ai_visual_content_moderator'
}

# Azure Configuration
AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
AZURE_KEY = os.environ.get("AZURE_KEY")
vision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))


def validate_user(username, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if validate_user(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session['image_path'] = filepath
            return redirect(url_for('result'))

    return render_template('upload.html')


@app.route('/result')
def result():
    if 'username' not in session or 'image_path' not in session:
        return redirect(url_for('login'))

    image_path = session['image_path']
    image = Image.open(image_path)

    # Basic info
    analysis = {
        'filename': os.path.basename(image_path),
        'format': image.format,
        'size': image.size,
        'mode': image.mode
    }

    # Azure Computer Vision Analysis
    with open(image_path, 'rb') as image_stream:
        vision_result = vision_client.analyze_image_in_stream(
            image_stream,
            visual_features=[
                VisualFeatureTypes.tags,
                VisualFeatureTypes.description,
                VisualFeatureTypes.categories,
                VisualFeatureTypes.color,
                VisualFeatureTypes.objects,
                VisualFeatureTypes.adult
            ]
        )

    # Append AI analysis to dictionary
    analysis['objects'] = [{
        'name': obj.object_property,
        'location': {
            'x': obj.rectangle.x,
            'y': obj.rectangle.y,
            'w': obj.rectangle.w,
            'h': obj.rectangle.h
        }
    } for obj in vision_result.objects]

    analysis['tags'] = [{
        'name': tag.name,
        'confidence': round(tag.confidence * 100, 2)
    } for tag in vision_result.tags]

    analysis['landmarks'] = []
    analysis['scenes'] = []
    for category in vision_result.categories:
        if category.detail and category.detail.landmarks:
            for landmark in category.detail.landmarks:
                analysis['landmarks'].append({
                    'name': landmark.name,
                    'confidence': round(landmark.confidence * 100, 2)
                })
        else:
            analysis['scenes'].append({
                'name': category.name,
                'confidence': round(category.score * 100, 2)
            })

    analysis['moderation'] = {
        'is_adult_content': vision_result.adult.is_adult_content,
        'adult_score': round(vision_result.adult.adult_score * 100, 2),
        'is_racy_content': vision_result.adult.is_racy_content,
        'racy_score': round(vision_result.adult.racy_score * 100, 2),
        'is_gory_content': vision_result.adult.is_gory_content,
        'gore_score': round(vision_result.adult.gore_score * 100, 2)
    }

    analysis['colors'] = {
        'background': vision_result.color.dominant_color_background,
        'foreground': vision_result.color.dominant_color_foreground,
        'accent': f"#{vision_result.color.accent_color}",
        'dominant_colors': vision_result.color.dominant_colors
    }

    return render_template('result.html', analysis=analysis, image_url=image_path)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

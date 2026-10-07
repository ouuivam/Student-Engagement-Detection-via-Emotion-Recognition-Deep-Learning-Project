from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import cv2
from flask import jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ResNet50AU(nn.Module):
    def __init__(self, num_labels):
        super(ResNet50AU, self).__init__()
        self.base_model = models.resnet50(pretrained=True)
        num_ftrs = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_labels),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.base_model(x)

model_path = os.path.join(os.path.dirname(__file__), "models", "resnet50.pth")
model = ResNet50AU(num_labels=12)
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

au_labels = ['AU01', 'AU12', 'AU15', 'AU17', 'AU02', 'AU20', 'AU25', 'AU26', 'AU04', 'AU05', 'AU06', 'AU09']

EMOTION_AU_WEIGHTS = {
    "joy": {"AU06": 1.0, "AU12": 1.0},
    "sad": {"AU01": 0.7, "AU04": 1.0, "AU15": 0.6},
    "surprise": {"AU01": 0.6, "AU02": 0.6, "AU05": 0.8, "AU26": 0.6},
    "fear": {"AU01": 0.4, "AU02": 0.4, "AU04": 0.5, "AU05": 0.6, "AU20": 0.6, "AU26": 0.5},
    "anger": {"AU04": 0.7, "AU05": 0.6, "AU20": 0.6},
    "disgust": {"AU09": 0.8, "AU15": 0.7},
    "contempt": {"AU12": 0.6}
}

EMOTION_TO_ENGAGEMENT = {
    "joy": "engagé",
    "surprise": "engagé",
    "anger": "non engagé",
    "sad": "non engagé",
    "disgust": "non engagé",
    "fear": "non engagé",
    "contempt": "non engagé",
    "neutre": "engagé"
}

def determine_emotion_by_score(confidences_dict):
    emotion_scores = {}
    for emotion, aus_weights in EMOTION_AU_WEIGHTS.items():
        score = 0.0
        for au, weight in aus_weights.items():
            if au in confidences_dict:
                score += confidences_dict[au] * weight
        emotion_scores[emotion] = score

    best_emotion = max(emotion_scores, key=emotion_scores.get)
    best_score = emotion_scores[best_emotion]

    if best_score <= 0.2:
        best_emotion = "neutre"
        engagement = "engagé"
    else:
        engagement = EMOTION_TO_ENGAGEMENT.get(best_emotion, "engagé")

    return best_emotion, engagement, emotion_scores

def extract_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image_cv = cv2.imread(image_path)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return image_path  # Aucun visage détecté, retourne l'image entière

    x, y, w, h = faces[0]
    face = image_cv[y:y+h, x:x+w]

    # Préparer le chemin pour enregistrer le visage recadré dans le dossier uploads
    base, ext = os.path.splitext(image_path)
    face_path = f"{base}_face{ext}"
    cv2.imwrite(face_path, face)

    return face_path

def predict_aus_and_emotion(image_path):
    face_path = extract_face(image_path)

    # Vérifie si c'est le même chemin = aucun visage détecté
    if face_path == image_path:
        confidences_dict = {au: 0.0 for au in au_labels}
        emotion = "inconnu"
        engagement = "inconnu"
        emotion_scores = {}
        return list(confidences_dict.items()), emotion, engagement, emotion_scores, image_path

    # Si visage détecté
    image = Image.open(face_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor).squeeze(0).numpy()

    confidences_dict = {au: float(score) for au, score in zip(au_labels, outputs)}
    emotion, engagement, emotion_scores = determine_emotion_by_score(confidences_dict)

    return list(confidences_dict.items()), emotion, engagement, emotion_scores, face_path



import cv2
import numpy as np
from PIL import Image
import io
from flask import Response

def predict_aus_on_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    annotated_frame = frame.copy()

    if len(faces) == 0:
        text = "Emotion: inconnu, Engagement: inconnu"
        cv2.putText(annotated_frame, text, (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return annotated_frame, "inconnu", "inconnu"

    x, y, w, h = faces[0]
    face_img = rgb_frame[y:y+h, x:x+w]
    pil_face = Image.fromarray(face_img)
    input_tensor = transform(pil_face).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor).squeeze(0).numpy()

    confidences_dict = {au: float(score) for au, score in zip(au_labels, outputs)}
    emotion, engagement, _ = determine_emotion_by_score(confidences_dict)

    cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    text = f"Emotion: {emotion}, Engagement: {engagement}"
    cv2.putText(annotated_frame, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    y0 = y + h + 20
    for i, (au, score) in enumerate(confidences_dict.items()):
        cv2.putText(annotated_frame, f"{au}: {score:.2f}", (x, y0 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    return annotated_frame, emotion, engagement


def gen_frames():
    cap = cv2.VideoCapture(0)  # Webcam locale

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame, emotion, engagement = predict_aus_on_frame(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/detecte') 
def detecte():
    return render_template('detecte.html') 



@app.route('/camera') 
def camera():
    return render_template('camera.html')  

@app.route('/feed_video')  
def feed_video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/teste', methods=['GET', 'POST'])
def teste():
    predictions = []
    filename = None
    detected_emotion = None
    engagement = None
    emotion_scores = {}

    if request.method == 'POST':
        file = request.files['image']
        if file:
            original_filename = secure_filename(file.filename)
            cleaned_filename = original_filename.replace(' ', '_')
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], cleaned_filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)

            predictions, detected_emotion, engagement, emotion_scores, face_path = predict_aus_and_emotion(save_path)

            # Extraire le chemin relatif à 'static/' pour url_for
            filename = os.path.relpath(face_path, start='static').replace('\\', '/')

    return render_template('teste.html',
                           filename=filename,
                           predictions=predictions,
                           emotion=detected_emotion,
                           engagement=engagement,
                           emotion_scores=emotion_scores)

@app.route('/predict_camera', methods=['POST'])
def predict_camera():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame uploaded'}), 400

    frame = request.files['frame']
    frame_path = os.path.join(app.config['UPLOAD_FOLDER'], 'webcam_frame.jpg')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    frame.save(frame_path)

    predictions, detected_emotion, engagement, emotion_scores, face_path = predict_aus_and_emotion(frame_path)

    return jsonify({
        'predictions': predictions,
        'emotion': detected_emotion,
        'engagement': engagement,
        'emotion_scores': emotion_scores
    })

@app.route('/live')
def live():
    return render_template('video_feed.html')

if __name__ == '__main__':
    app.run(debug=True)

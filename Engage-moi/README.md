🎓 Engage-Moi — Student Engagement Detection via Emotion Recognition

Système intelligent de détection de l'engagement des étudiants basé sur la reconnaissance des émotions et des Action Units (AUs).
<img width="1891" height="897" alt="image" src="https://github.com/user-attachments/assets/44a37f93-ccb8-478b-986d-edb7c82339c1" />
📌 Présentation

Engage-Moi est une application web basée sur l'Intelligence Artificielle permettant d'analyser les expressions faciales d'un étudiant afin d'identifier ses Action Units (AUs), d'estimer son état émotionnel, puis de déduire un niveau d'engagement.

Le système combine :

Deep Learning avec ResNet50 ;

Computer Vision avec OpenCV ;

Facial Detection avec Haar Cascade ;

Action Unit Recognition ;

une couche d'interprétation des émotions ;

une classification de l'engagement ;

une interface web développée avec Flask.

L'application permet également une analyse à partir de la webcam en temps réel.


Le projet vise à développer une solution capable de :

détecter automatiquement un visage dans une image ;

extraire la région faciale ;

prédire plusieurs Action Units ;

interpréter les AUs afin d'estimer une émotion ;

déduire un état d'engagement ;

afficher les résultats dans une interface web intuitive ;

analyser les expressions faciales à partir d'une webcam.

😊 Détection des émotions

Les Action Units prédites sont utilisées pour calculer des scores correspondant à différentes émotions.

Les émotions considérées sont :

Joy

Sad

Surprise

Fear

Anger

Disgust

Contempt

Neutre

Chaque émotion est associée à un ensemble d'Action Units pondérées.

🎓 Détection de l'engagement

Une règle d'interprétation permet ensuite d'associer l'émotion détectée à un état d'engagement.

Émotion

Engagement

Joy

Engagé

Surprise

Engagé

Neutre

Engagé

Sad

Non engagé

Fear

Non engagé

Anger

Non engagé

Disgust

Non engagé

Contempt

Non engagé

Cette étape constitue une règle d'interprétation basée sur les émotions et non un modèle de classification de l'engagement entraîné directement sur des données d'engagement.

📸 Analyse d'une image

L'utilisateur peut importer une image contenant un visage.

Le système :

charge l'image ;

détecte le visage ;

encadre le visage détecté en rouge ;

conserve l'image complète pour l'affichage ;

extrait le visage pour l'analyse ;

applique le modèle ResNet50 ;

prédit les Action Units ;

calcule les scores émotionnels ;

affiche l'émotion et l'engagement.

L'interface affiche notamment :

l'image complète analysée ;

le visage détecté ;

les Action Units ;

leur intensité ;

les scores des émotions ;

l'émotion finale ;

l'état d'engagement.

<img width="1891" height="911" alt="image" src="https://github.com/user-attachments/assets/82196e5d-ea58-43b9-9bdd-c14480bbdf40" />
<img width="1796" height="907" alt="image" src="https://github.com/user-attachments/assets/7e3b63b7-a885-408c-9700-4b246cc23d4c" />

📁 Structure du projet

Engage-moi/
│
├── app2.py
│
├── models/
│   └── resnet50.pth
│
├── templates/
│   ├── index.html
│   ├── detecte.html
│   ├── teste.html
│   ├── camera.html
│   ├── video_feed.html
│   ├── header.html
│   └── footer.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── image/
│   └── uploads/
│
├── requirements.txt
├── .gitignore
└── README.md

La structure exacte peut évoluer selon les fichiers présents dans le projet.

🛠️ Technologies utilisées

Intelligence Artificielle

Python

PyTorch

Torchvision

ResNet50

Deep Learning

Action Unit Recognition

Computer Vision

OpenCV

Haar Cascade

Image preprocessing

Facial detection

Webcam processing

Backend

Flask

Python

Frontend

HTML5

CSS3

JavaScript

Outils

Git

GitHub

Virtual Environment (venv)

⚙️ Installation

1. Cloner le projet

git clone https://github.com/<USERNAME>/<REPOSITORY>.git
cd Engage-moi

Remplacez <USERNAME> et <REPOSITORY> par les informations de votre dépôt GitHub.

2. Créer un environnement virtuel

Avec Python 3.11 :

py -3.11 -m venv venv

3. Activer l'environnement virtuel

Sous Windows PowerShell :

.\venv\Scripts\Activate.ps1

Sous Windows CMD :

venv\Scripts\activate

4. Installer les dépendances

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

▶️ Lancer l'application

Une fois l'environnement activé :

python app2.py

Flask démarre ensuite le serveur local.

Ouvrir dans le navigateur :

http://127.0.0.1:5000



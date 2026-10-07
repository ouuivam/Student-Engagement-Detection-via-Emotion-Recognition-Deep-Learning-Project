# 🎓 Engage-Moi — Student Engagement Detection via Emotion Recognition

> Système intelligent de détection de l'engagement des étudiants basé sur la reconnaissance des émotions et des Action Units (AUs).

<img width="1891" height="897" alt="image" src="https://github.com/user-attachments/assets/44a37f93-ccb8-478b-986d-edb7c82339c1" />

## 📌 Présentation

**Engage-Moi** est une application web basée sur l'Intelligence Artificielle permettant d'analyser les expressions faciales d'un étudiant afin de détecter ses **Action Units (AUs)**, d'estimer son **émotion**, puis de déduire son niveau d'**engagement**.

Le système combine **Deep Learning**, **Computer Vision** et **reconnaissance des émotions** à travers un modèle **ResNet50** et OpenCV.

L'application permet également une analyse à partir de la **webcam en temps réel**.

## 🎯 Objectifs

- Détecter automatiquement le visage dans une image ou une vidéo.
- Prédire les Action Units et leurs intensités.
- Estimer l'émotion à partir des AUs détectées.
- Déduire un état d'engagement.
- Afficher les résultats dans une interface web.
- Permettre l'analyse en temps réel via webcam.

## 🌐 Fonctionnalités du site

### 📸 Analyse d'une image

L'utilisateur peut importer une image contenant un visage.

Le système :

1. détecte le visage ;
2. l'encadre en **rouge** sur l'image complète ;
3. extrait la région faciale pour l'analyse ;
4. applique le modèle **ResNet50** ;
5. prédit les Action Units ;
6. calcule les scores émotionnels ;
7. affiche l'émotion et l'engagement estimés.

<img width="1891" height="911" alt="image" src="https://github.com/user-attachments/assets/82196e5d-ea58-43b9-9bdd-c14480bbdf40" />

<img width="1796" height="907" alt="image" src="https://github.com/user-attachments/assets/7e3b63b7-a885-408c-9700-4b246cc23d4c" />

### 🎥 Analyse par webcam

L'application permet également d'utiliser la webcam pour analyser les expressions faciales **en temps réel** et afficher l'émotion ainsi que l'état d'engagement détectés.

## 🛠️ Technologies utilisées

| Catégorie | Technologies |
|---|---|
| **IA / Deep Learning** | Python, PyTorch, Torchvision, ResNet50 |
| **Computer Vision** | OpenCV, Haar Cascade |
| **Backend** | Flask |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Outils** | Git, GitHub, Virtual Environment (venv) |

## 📁 Structure du projet

```text
Engage-moi/
│
├── app2.py
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
```

## ⚙️ Installation

### 1. Cloner le projet

```bash
cd Engage-moi
```

### 2. Créer l'environnement virtuel

Python **3.11** est recommandé.

```bash
py -3.11 -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows PowerShell :**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD :**

```cmd
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## ▶️ Lancer l'application

Une fois l'environnement virtuel activé :

```bash
python app2.py
```

Puis ouvrir :

```text
http://127.0.0.1:5000
```

## 👩‍💻 Projet académique

**Engage-Moi** est réalisé dans le cadre d'un projet académique en **Intelligence Artificielle**, avec un focus sur le **Deep Learning**, la **Computer Vision**, la **reconnaissance des émotions** et la **détection de l'engagement étudiant**.


<3
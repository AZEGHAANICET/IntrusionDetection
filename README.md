```markdown
# Détecteur d'Intrusions Réseau - Application Streamlit

## 🚀 Présentation

Ce projet propose une **application web professionnelle** permettant de détecter des **intrusions ou anomalies dans le trafic réseau**. Elle est basée sur des **modèles de machine learning classiques** (Logistic Regression, Random Forest, Naive Bayes, KNN, SVC, Decision Tree, Gradient Boosting) ainsi qu'un **modèle LSTM** pour capturer les séquences temporelles.

L'application est développée avec **Streamlit**, offrant une interface moderne, interactive et intuitive pour les utilisateurs.

## 📁 Structure du projet

```

intrusion\_app/
│
├── models/                  # Contient les modèles entraînés (.joblib et .h5)
├── app.py     # Application Streamlit principale
├── requirements.txt               # Dépendances Python
└── README.md                      # Ce fichier

````

## 🛠 Fonctionnalités principales

1. **Choix du modèle** : sélectionner parmi tous les modèles sauvegardés.
2. **Méthodes d'entrée** :
   - Upload d'un fichier CSV contenant les features.
   - Entrée manuelle des features via la sidebar avec descriptions.
3. **Prédictions** :
   - Affichage des prédictions dans un tableau interactif.
   - Visualisation graphique de la distribution des prédictions.
4. **Téléchargement** : possibilité de télécharger les résultats en CSV.

## 📊 Features utilisées

- `srcip_count` : Nombre total de connexions par IP source.
- `srcip_unique_dst` : Nombre de destinations uniques par IP source.
- `srcip_avg_bytes_sent` : Moyenne des octets envoyés.
- `srcip_avg_bytes_received` : Moyenne des octets reçus.
- `srcip_std_bytes_sent` : Écart-type des octets envoyés.
- `srcip_std_bytes_received` : Écart-type des octets reçus.
- `bytes_ratio` : Ratio octets envoyés / reçus.
- `bytes_ratio_log` : Logarithme du ratio.
- `dstport_critical` : 1 si le port est critique, 0 sinon.
- `hour` : Heure de la connexion (0-23).
- `multi_target_ratio` : Ratio destinations uniques / connexions totales.

## ⚙️ Installation

1. Créez un environnement virtuel (recommandé) :

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
````

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancez l'application Streamlit :

```bash
streamlit run streamlit_intrusion_app.py
```

## 🧩 Utilisation

1. Ouvrez la sidebar pour sélectionner le modèle.
2. Choisissez la méthode d'entrée : upload CSV ou entrée manuelle.
3. Cliquez sur `🔍 Prédire`.
4. Consultez les résultats et graphiques.
5. Téléchargez le CSV des prédictions si nécessaire.

## 📌 Remarques

* Les modèles doivent être préalablement entraînés et sauvegardés dans le dossier `saved_models/`.
* LSTM nécessite des features en format 3D (reshaping effectué automatiquement dans l'application).

## 🔗 Liens et références

* [Streamlit](https://streamlit.io/)
* [Scikit-learn](https://scikit-learn.org/)
* [TensorFlow](https://www.tensorflow.org/)
* [Seaborn](https://seaborn.pydata.org/)

## 👨‍💻 Auteur

Projet développé par Anicet Loïc - Détection d'intrusions et visualisation réseau.

```
```

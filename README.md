# Détecteur d'Intrusions Réseau - Application Streamlit

## 🚀 Présentation

Ce projet propose une **application web professionnelle** permettant de détecter des **intrusions ou anomalies dans le trafic réseau**.  
Elle repose sur des **modèles de machine learning classiques** (Logistic Regression, Random Forest, Naive Bayes, KNN, SVC, Decision Tree, Gradient Boosting) ainsi qu'un **modèle LSTM** pour capturer les séquences temporelles.

L'application est développée avec **Streamlit**, offrant une interface moderne, interactive et intuitive pour les utilisateurs.

---

## 📁 Structure du projet

```plaintext
intrusion_app/
│
├── models/                              # Contient les modèles entraînés (.joblib et .h5)
├── app.py                               # Application Streamlit principale
├── requirements.txt                     # Dépendances Python
└── README.md                            # Ce fichier
└── ML                                   (construction du Modèle)
└── fichier fortigate_logs_dataset_Camtel.csv (Notre dataset)
```

## 🛠 Fonctionnalités principales

1. **Choix du modèle** : sélection parmi tous les modèles sauvegardés.
2. **Méthodes d'entrée** :
   - Upload d'un fichier CSV contenant les données brutes.
   - Entrée manuelle via la sidebar avec des descriptions pour guider l'utilisateur.
   - Génération aléatoire de données pour tester rapidement.
3. **Prédictions** :
   - Résultats affichés dans un tableau interactif.
   - Visualisation graphique de la distribution des prédictions.
   - Explications textuelles des comportements détectés.
4. **Téléchargement** : export des résultats au format CSV.

---

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
- (D’autres features avancées comme l’entropie, l’activité nocturne, etc. peuvent être calculées en arrière-plan pour enrichir les analyses).

---

## ⚙️ Installation

1. Créez un environnement virtuel (recommandé) :

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```
2. Installez les dépendances
```bash
pip install -r requirements.txt
```
3. Lancez l'application Streamlit
```bash
streamlit run app.py
```



---
## 🔄 Pipeline de traitement

```mermaid
 flowchart TD
    A[📂 Données brutes] --> B[⚙️ Prétraitement]
    B --> C[🧠 Modèles ML/DL]
    C --> D[📊 Résultats prédits]
    D --> E[📈 Visualisation]
    D --> F[📥 Export CSV]
    
    A -->|CSV / Manuel / Aléatoire| B
    B -->|Nettoyage / Normalisation| C
    C -->|Prédictions| D
    D -->|Graphiques / Tableaux| E
    D -->|Téléchargement| F
```
---

## 🛠 Fonctionnalités principales

1. **Choix du modèle** : sélection parmi tous les modèles sauvegardés.  
2. **Méthodes d'entrée** :  
   - Upload d'un fichier CSV contenant les données brutes.  
   - Entrée manuelle via la sidebar avec des descriptions pour guider l'utilisateur.  
   - Génération aléatoire de données pour tester rapidement.  
3. **Prédictions** :  
   - Résultats affichés dans un tableau interactif.  
   - Visualisation graphique de la distribution des prédictions.  
   - Explications textuelles des comportements détectés.  
4. **Téléchargement** : export des résultats au format CSV.  

---






import streamlit as st
import pandas as pd
import numpy as np
import os
import random
import time
from joblib import load
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Configuration page
# -------------------------------
st.set_page_config(
    page_title="Détecteur d'Intrusions Réseau",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Détecteur d'Intrusions Réseau")
st.markdown("""
Application pour détecter les **trafics réseau suspects**.  
Modes disponibles : **CSV**, **entrée manuelle**, **génération aléatoire**.
""")

# -------------------------------
# Sidebar : choix modèle
# -------------------------------
st.sidebar.header("Configuration")
model_options = [f.replace('_model.joblib', '').replace('_', ' ')
                 for f in os.listdir('models') if f.endswith('.joblib')] + ['LSTM']
selected_model_name = st.sidebar.selectbox("Choisir le modèle", model_options)

# -------------------------------
# Gestion Input
# -------------------------------
input_method = st.sidebar.radio("Méthode d'entrée", ["Uploader un CSV", "Entrée manuelle", "Générer aléatoire"])
df_input = None

# --- CSV
if input_method == "Uploader un CSV":
    st.sidebar.info("Le CSV doit contenir : srcip, dstip, bytes_sent, bytes_received, dstport, time (HH:MM:SS).")
    uploaded_file = st.file_uploader("Uploader CSV", type=['csv'])
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file)

# --- Entrée manuelle
elif input_method == "Entrée manuelle":
    st.sidebar.markdown("### Entrée manuelle")
    raw_cols = ["srcip", "dstip", "bytes_sent", "bytes_received", "dstport", "time"]
    input_labels = {
        "srcip": "IP source", "dstip": "IP destination",
        "bytes_sent": "Octets envoyés", "bytes_received": "Octets reçus",
        "dstport": "Port de destination", "time": "Heure (HH:MM:SS)"
    }
    manual_data = {}
    for col in raw_cols:
        if col in ["bytes_sent", "bytes_received", "dstport"]:
            manual_data[col] = st.sidebar.number_input(input_labels[col], value=0)
        else:
            default = "00:00:00" if col == "time" else "0.0"
            manual_data[col] = st.sidebar.text_input(input_labels[col], value=default)
    df_input = pd.DataFrame([manual_data])

# --- Génération aléatoire avec session_state
elif input_method == "Générer aléatoire":
    st.sidebar.markdown("### Génération aléatoire")

    def generate_random_event():
        srcip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        dstip = f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
        bytes_sent = random.randint(0, 10000)
        bytes_received = random.randint(0, 10000)
        dstport = random.choice([22, 23, 25, 53, 80, 443, 445, random.randint(1024, 65535)])
        hour = random.randint(0, 23)
        time_str = f"{hour:02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        return {"srcip": srcip, "dstip": dstip, "bytes_sent": bytes_sent,
                "bytes_received": bytes_received, "dstport": dstport, "time": time_str}

    if "random_event" not in st.session_state:
        st.session_state["random_event"] = None

    if st.sidebar.button("🎲 Générer un événement"):
        st.session_state["random_event"] = generate_random_event()

    if st.session_state["random_event"] is not None:
        df_input = pd.DataFrame([st.session_state["random_event"]])
        st.sidebar.subheader("Valeurs générées")
        st.sidebar.json(st.session_state["random_event"])

# -------------------------------
# Feature Engineering
# -------------------------------
def compute_features(df):
    df = df.copy()
    df["srcip_count"] = df.groupby("srcip")["srcip"].transform("count")
    df["srcip_unique_dst"] = df.groupby("srcip")["dstip"].transform("nunique")
    df["srcip_avg_bytes_sent"] = df.groupby("srcip")["bytes_sent"].transform("mean")
    df["srcip_avg_bytes_received"] = df.groupby("srcip")["bytes_received"].transform("mean")
    df["srcip_std_bytes_sent"] = df.groupby("srcip")["bytes_sent"].transform("std").fillna(0)
    df["srcip_std_bytes_received"] = df.groupby("srcip")["bytes_received"].transform("std").fillna(0)
    df["bytes_ratio"] = df["bytes_sent"] / (df["bytes_received"] + 1)
    df["bytes_ratio_log"] = np.log1p(df["bytes_ratio"])
    critical_ports = {22, 23, 25, 53, 80, 443, 445}
    df["dstport_critical"] = df["dstport"].isin(critical_ports).astype(int)

    def safe_hour(t):
        try:
            return int(str(t).split(":")[0])
        except:
            return 0

    df["hour"] = df["time"].apply(safe_hour)
    df["multi_target_ratio"] = df["srcip_unique_dst"] / (df["srcip_count"] + 1)
    df["critical_port_count"] = df.groupby("srcip")["dstport_critical"].transform("sum")
    df["night_activity"] = df["hour"].apply(lambda x: int(x < 6 or x >= 22))
    df["avg_packet_size"] = (df["bytes_sent"] + df["bytes_received"]) / df["srcip_count"]

    def entropy(x):
        counts = x.value_counts(normalize=True)
        return -np.sum(counts * np.log2(counts + 1e-9))

    df["dst_entropy"] = df.groupby("srcip")["dstip"].transform(entropy)

    feature_cols = [
        "srcip_count", "srcip_unique_dst", "srcip_avg_bytes_sent", "srcip_avg_bytes_received",
        "srcip_std_bytes_sent", "srcip_std_bytes_received", "bytes_ratio", "bytes_ratio_log",
        "dstport_critical", "hour", "multi_target_ratio"
    ]
    return df, feature_cols

# -------------------------------
# Explication
# -------------------------------
def explain_event(row):
    reasons = []
    if "dstport_critical" in row and row["dstport_critical"]: reasons.append("Port critique utilisé")
    if "night_activity" in row and row["night_activity"]: reasons.append("Activité nocturne")
    if "multi_target_ratio" in row and row["multi_target_ratio"] > 0.5: reasons.append("Connexion à plusieurs destinations")
    if "bytes_ratio" in row and row["bytes_ratio"] > 2: reasons.append("Ratio bytes anormal")
    if "dst_entropy" in row and row["dst_entropy"] > 2: reasons.append("Diversité destinations élevée")
    return ", ".join(reasons) if reasons else "Aucun comportement anormal détecté"

# -------------------------------
# Prédiction
# -------------------------------
if df_input is not None and st.button("🔍 Prédire"):
    with st.spinner("🛠 Calcul des features et prédiction..."):
        time.sleep(1)
        X_all, feature_cols = compute_features(df_input)

        X_model = X_all[feature_cols]

        if selected_model_name == "LSTM":
            model = load_model(os.path.join('models', 'LSTM_model.h5'))
            scaler_path = os.path.join('models', 'scaler.joblib')
            if os.path.exists(scaler_path):
                scaler = load(scaler_path)
                X_model = pd.DataFrame(scaler.transform(X_model), columns=X_model.columns)
            X_rnn = X_model.values.reshape((X_model.shape[0], 1, X_model.shape[1]))
            y_prob = model.predict(X_rnn)
            y_pred = tf.argmax(y_prob, axis=1).numpy()
            risk = tf.reduce_max(y_prob, axis=1).numpy() * 100
        else:
            model = load(os.path.join('models', f"{selected_model_name.replace(' ', '_')}_model.joblib"))
            scaler_path = os.path.join('models', 'scaler.joblib')
            if os.path.exists(scaler_path):
                scaler = load(scaler_path)
                X_model = pd.DataFrame(scaler.transform(X_model), columns=X_model.columns)
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_model)
                y_pred = np.argmax(y_prob, axis=1)
                risk = np.max(y_prob, axis=1) * 100
            else:
                y_pred = model.predict(X_model)
                risk = np.array([100 if p == 1 else 0 for p in y_pred])

        df_input["Prediction"] = ["🚨 Intrusion détectée !" if p == 1 else "✅ Trafic normal" for p in y_pred]
        df_input["Risque (%)"] = risk.round(2)
        df_input["Explication"] = X_all.apply(explain_event, axis=1)

    st.success("✅ Prédiction terminée !")

    if input_method == "Uploader un CSV":
        st.subheader("Résultats (CSV)")
        st.dataframe(df_input)

        st.subheader("Distribution des prédictions")
        fig, ax = plt.subplots()
        sns.countplot(x="Prediction", data=df_input, palette="viridis", ax=ax)
        st.pyplot(fig)

        st.subheader("Corrélation des features")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.heatmap(X_all.corr(), annot=False, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)

    elif input_method == "Entrée manuelle":
        st.subheader("Résultat (Entrée unique)")
        st.write(df_input[["srcip", "dstip", "Prediction", "Risque (%)", "Explication"]])

    elif input_method == "Générer aléatoire":
        st.subheader("Résultat (Événement généré)")
        st.json(df_input[["srcip", "dstip", "dstport", "Prediction", "Risque (%)", "Explication"]].iloc[0].to_dict())

    csv = df_input.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger résultats (CSV)", data=csv, file_name="predictions.csv", mime="text/csv")

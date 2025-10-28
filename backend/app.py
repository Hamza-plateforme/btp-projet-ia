
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline


app = Flask(__name__)
CORS(app)
DB_FILE = "historique_feedbacks.json"


# Pipeline HuggingFace pour analyse sentiment multilingue (français inclus)
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")


def suggestion_contextuelle(feedback, emotion):
    txt = feedback.lower()
    if "malade" in txt or "fièvre" in txt:
        return "Soigne-toi bien et prends du repos. Consulte un professionnel de santé si nécessaire."
    if "fatigue" in txt or "fatigué" in txt:
        return "N'oublie pas de te reposer et de bien dormir pour récupérer."
    if "bloqué" in txt or "bloquer" in txt or "difficile" in txt or "pas réussi" in txt or "peur" in txt:
        return "N’hésite pas à demander de l’aide à ton équipe ou à ton manager."
    if "démotivé" in txt or "motivation" in txt:
        return "Partage tes ressentis, fixe-toi des objectifs simples et sollicite le soutien de ton équipe."
    if "pas compris" in txt or "incompréhensible" in txt or "complexe" in txt or "trop rapide" in txt:
        return "Pose toutes tes questions, reformule les points flous ou consulte la documentation."
    if "charge" in txt and ("travail" in txt or "trop" in txt):
        return "Si la charge de travail est trop lourde, communique avec ton équipe pour une meilleure répartition."
    if "merci" in txt or "bravo" in txt or emotion == "positif":
        return "Merci pour ton énergie positive, continue ainsi !"
    if "retard" in txt or "deadline" in txt or "pas fini" in txt:
        return "Ne te décourage pas, planifie bien ton travail et communique sur ta progression."
    if emotion == "négatif":
        return "Identifie les difficultés et discute avec ton équipe pour trouver des solutions."
    if emotion == "positif":
        return "Bravo pour ta motivation et ton engagement !"
    if emotion == "neutre":
        return "Merci pour ton retour, chaque avis compte."
    return "Merci pour ton retour, toutes les remarques sont précieuses."


@app.route('/')
def home():
    return "RetroMind API opérationnelle !"


@app.route('/analyse-feedback', methods=['POST'])
def analyse_feedback():
    data = request.get_json()
    feedback = data.get('feedback', '')

    analyse = sentiment_pipeline(feedback)[0]
    label = analyse['label']
    score = analyse['score']
    stars = int(label.split()[0])

    if stars >= 4:
        emotion = "positif"
    elif stars == 3:
        emotion = "neutre"
    else:
        emotion = "négatif"

    suggestion = suggestion_contextuelle(feedback, emotion)

    synthese = feedback.split('.')[0]
    mots = [w for w in feedback.split() if len(w) >= 4]
    theme = mots[0] if mots else ""

    result = {
        'feedback': feedback,
        'synthese': synthese,
        'emotion': emotion,
        'theme': theme,
        'suggestion': suggestion,
        'score': score
    }

    historique = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            historique = json.load(f)
    historique.append(result)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)

    return jsonify(result)


@app.route('/historique', methods=['GET'])
def get_historique():
    if not os.path.exists(DB_FILE):
        return jsonify([])
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        historique = json.load(f)
    return jsonify(historique)


if __name__ == '__main__':
    app.run(debug=True)






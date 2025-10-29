<!-- Animation SVG en haut pour une « animation fluide » visible sur GitHub/VSCode -->
<div align="center">
	<svg width="640" height="120" viewBox="0 0 640 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
		<defs>
			<linearGradient id="g" x1="0" x2="1">
				<stop offset="0%" stop-color="#6EE7B7"/>
				<stop offset="50%" stop-color="#60A5FA"/>
				<stop offset="100%" stop-color="#A78BFA"/>
			</linearGradient>
		</defs>
		<rect width="100%" height="100%" rx="12" fill="#0f172a" />
		<!-- moving circles -->
		<g fill="url(#g)" opacity="0.95">
			<circle cx="80" cy="60" r="12">
				<animate attributeName="cx" dur="6s" values="-40;720" repeatCount="indefinite" />
				<animate attributeName="r" dur="3s" values="8;14;8" repeatCount="indefinite" />
			</circle>
			<circle cx="160" cy="40" r="10">
				<animate attributeName="cx" dur="5s" values="-60;720" repeatCount="indefinite" begin="-1s"/>
				<animate attributeName="cy" dur="4s" values="20;80;20" repeatCount="indefinite"/>
			</circle>
			<circle cx="240" cy="80" r="14">
				<animate attributeName="cx" dur="7s" values="-120;720" repeatCount="indefinite" begin="-0.5s"/>
				<animate attributeName="r" dur="3.5s" values="12;18;12" repeatCount="indefinite"/>
			</circle>
			<circle cx="360" cy="60" r="9">
				<animate attributeName="cx" dur="4.8s" values="-20;720" repeatCount="indefinite" begin="-0.8s"/>
				<animate attributeName="cy" dur="6s" values="80;30;80" repeatCount="indefinite"/>
			</circle>
			<circle cx="520" cy="50" r="11">
				<animate attributeName="cx" dur="6.5s" values="-100;720" repeatCount="indefinite" begin="-1.6s"/>
				<animate attributeName="r" dur="3s" values="10;16;10" repeatCount="indefinite"/>
			</circle>
		</g>
		<text x="50%" y="50%" fill="#e6eef8" font-size="18" font-family="Segoe UI, Roboto, Arial" text-anchor="middle" dominant-baseline="middle">RetroMind — Feedback & Sentiment</text>
	</svg>
</div>

# RetroMind

Petit projet de prototype pour l'analyse de feedbacks et la synthèse de suggestions (interface Next.js + API Flask + pipeline HuggingFace).

## Vue d'ensemble

- Backend: `backend/app.py` — API Flask qui expose trois endpoints principaux :
	- `GET /` : route racine (statut)
	- `POST /analyse-feedback` : reçoit JSON `{ "feedback": "..." }`, applique un pipeline HuggingFace (modèle `nlptown/bert-base-multilingual-uncased-sentiment`) et retourne `{ feedback, synthese, emotion, theme, suggestion, score }`. Le backend enregistre également l'historique dans `backend/historique_feedbacks.json`.
	- `GET /historique` : renvoie l'historique des analyses (fichier JSON local).

## Pourquoi cette structure

- Prototype simple et autonome : récupérer un feedback -> analyser -> proposer une suggestion contextuelle -> garder un historique local. Cible pédagogique / PoC.
- Découplage frontend/backend : l'API est kleine et peut être remplacée ou conteneurisée sans toucher au frontend.

## Fichiers clés à consulter

- `backend/app.py` — logique d'analyse, pipeline HF, règles de suggestion (fonction `suggestion_contextuelle`).
- `backend/historique_feedbacks.json` — stockage local (peut être absent au démarrage).
- `frontend/src/app/` — pages Next.js (exemples d'appels fetch vers l'API).
- `docker/` — (présence possible) contient fichiers pratiques pour conteneurisation si vous voulez déployer.

## Exemples d'appel API

POST /analyse-feedback

Request JSON:

{
	"feedback": "Je suis un peu fatigué et bloqué sur la tâche X, merci pour le soutien"
}

Réponse (extrait):

{
	"feedback": "...",
	"synthese": "Je suis un peu fatigué et bloqué sur la tâche X",
	"emotion": "négatif",
	"theme": "je",
	"suggestion": "N'oublie pas de te reposer...",
	"score": 0.85
}

## Commandes rapides (dev)

Backend (Windows PowerShell) — recommandations :

```powershell
cd btp-projet-ia\backend
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install flask transformers "torch"  # torch peut être requis selon la plateforme
python app.py
```

Frontend (Next.js) :

```powershell
cd btp-projet-ia\frontend
npm install
npm run dev
```

## Limitations connues

- Pas d'authentification ni de contrôle d'accès.
- Le parsing du `theme` et la synthèse sont très basiques (heuristiques à améliorer pour production).
- `transformers` + `torch` peuvent augmenter fortement l'empreinte disque et mémoire.

## Besoin d'aide / Prochaines étapes possibles

- Ajouter un `requirements.txt` dans `backend/` pour simplifier l'installation.
- Remplacer le stockage JSON par une petite DB (SQLite / PostgreSQL) si concurrence attendue.
- Ajouter tests unitaires pour la logique dans `suggestion_contextuelle`.

---

Si tu veux, j'adapte le texte (fr/en), j'ajoute un GIF animé personnalisé, ou je crée un `requirements.txt` et un script d'initialisation `setup-dev.ps1` pour automatiser l'installation sur Windows.

Dis-moi quelle variante tu préfères et je l'ajoute !

# Todo API

API REST simple pour gérer une liste de tâches (Todo), construite avec Flask et SQLite.

## Installation

```bash
cd todo-api
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Lancer l'application

```bash
python app.py
```

L'application démarre sur `http://localhost:5000` et crée automatiquement la base de données SQLite (`todos.db`) au premier lancement.

## Exécuter les tests

```bash
pytest test_app.py -v
```

Les tests utilisent une base de données SQLite temporaire distincte (`tempfile`) pour ne pas affecter `todos.db`.

![Résultats des tests](screenshots/tests.png)

## Endpoints de l'API

| Méthode | Endpoint            | Description                          |
|---------|----------------------|---------------------------------------|
| GET     | `/todos`             | Liste toutes les tâches               |
| POST    | `/todos`             | Crée une nouvelle tâche               |
| GET     | `/todos/<id>`        | Récupère une tâche par son ID         |
| PUT     | `/todos/<id>`        | Met à jour une tâche existante        |
| DELETE  | `/todos/<id>`        | Supprime une tâche                    |

### Exemples avec curl

```bash
# Créer une tâche
curl -X POST -H "Content-Type: application/json" \
  -d '{"title": "Apprendre DevSecOps", "description": "Module 4 TP"}' \
  http://localhost:5000/todos

# Lister les tâches
curl http://localhost:5000/todos

# Récupérer une tâche
curl http://localhost:5000/todos/1

# Mettre à jour une tâche
curl -X PUT -H "Content-Type: application/json" \
  -d '{"title": "Apprendre DevSecOps - Mise à jour", "done": true}' \
  http://localhost:5000/todos/1

# Supprimer une tâche
curl -X DELETE http://localhost:5000/todos/1
```

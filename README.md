# API REST de réservations hôtelières

Projet de développement à base de composants et services web.

## Technologies prévues

- Python et Flask
- PostgreSQL
- SQLAlchemy et Marshmallow
- Apache NiFi
- Postman et Pytest
- Docker Compose

## Démarrage local

Depuis l'invite de commandes Windows (`cmd`) :

```cmd
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
copy .env.example .env
python run.py
```

Avant le démarrage, modifiez `.env` et remplacez `VOTRE_MOT_DE_PASSE` par le
mot de passe PostgreSQL local. La base `hotel_reservation` doit exister.

Pour créer les tables avec Flask-Migrate :

```cmd
flask --app run.py db upgrade
```

L'API est ensuite accessible aux adresses suivantes :

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/api/v1/health`

## Endpoints REST

Toutes les ressources prennent en charge les opérations CRUD :

| Ressource | Liste et création | Consultation, modification et suppression |
|---|---|---|
| Hôtels | `GET/POST /api/v1/hotels` | `GET/PUT/DELETE /api/v1/hotels/{id}` |
| Clients | `GET/POST /api/v1/clients` | `GET/PUT/DELETE /api/v1/clients/{id}` |
| Réservations | `GET/POST /api/v1/reservations` | `GET/PUT/DELETE /api/v1/reservations/{id}` |

Les routes de liste acceptent `page` et `per_page`. Les hôtels peuvent être
filtrés par `nom` et `ville`, les clients par `nom` et `email`, et les
réservations par `hotel_id`, `client_id`, `statut`, `date_debut` et `date_fin`.

Exemple :

```text
GET /api/v1/reservations?page=1&per_page=10&statut=CONFIRMEE
```

## Tests automatisés

```cmd
python -m pip install -r requirements-dev.txt
python -m pytest
```

## État du projet

Le squelette Flask, les modèles PostgreSQL, les migrations, les trois CRUD,
leurs validations et les premiers tests automatisés sont en place. Le flux
NiFi, les tests Postman, le contrat OpenAPI et la conteneurisation restent à
implémenter.

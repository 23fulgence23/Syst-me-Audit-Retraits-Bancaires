# 🏦 Système d'Audit des Retraits Bancaires
**Stack : Python Flask + Vue.js + MySQL (Laragon)**

---

## 📁 Structure du Projet

```
bank-audit/
├── sql/
│   └── setup.sql          ← Script SQL (tables + triggers)
├── backend/
│   ├── app.py             ← Serveur Flask (API REST)
│   └── requirements.txt   ← Dépendances Python
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── App.vue
        ├── services/api.js
        └── views/
            ├── Clients.vue
            ├── Retraits.vue  ← CRUD complet
            └── Audit.vue     ← Journal d'audit + stats
```

---

## ⚙️ ÉTAPE 1 — Configurer Laragon + MySQL

1. **Démarrer Laragon** et cliquer sur **"Start All"**
2. Cliquer sur **"HeidiSQL"** (ou Menu → MySQL)
3. Dans HeidiSQL, ouvrir un **Nouvel onglet de requête**
4. **Coller et exécuter** le contenu de `sql/setup.sql`
5. Vérifier que la base `bank_audit` est créée avec les 3 tables et les triggers

> ✅ Par défaut Laragon : host=`localhost`, user=`root`, password=`` (vide), port=`3306`

---

## ⚙️ ÉTAPE 2 — Lancer le Backend Python

```bash
cd backend

# Installer les dépendances (une seule fois)
pip install -r requirements.txt

# Lancer Flask
python app.py
```

Le serveur démarre sur **http://localhost:5000**

Tester : http://localhost:5000/api/health → doit retourner `{"status": "OK"}`

> 💡 Si vous avez un mot de passe MySQL dans Laragon, modifier `DB_CONFIG` dans `app.py` :
> ```python
> 'password': 'votre_mot_de_passe',
> ```

---

## ⚙️ ÉTAPE 3 — Lancer le Frontend Vue.js

```bash
cd frontend

# Installer les dépendances Node.js (une seule fois)
npm install

# Lancer le serveur de développement
npm run dev
```

L'application s'ouvre sur **http://localhost:3000**

---

## 🚀 Utilisation

| Page | Description |
|------|-------------|
| **Clients** | Voir les comptes clients et leurs soldes |
| **Retraits** | Créer, modifier, supprimer des retraits (CRUD) |
| **Audit** | Journal complet de toutes les opérations (INSERT/UPDATE/DELETE) |

### Fonctionnement des Triggers MySQL

| Opération | Ce qui se passe |
|-----------|----------------|
| **Créer** un retrait | Solde client diminue + enregistrement INSERT dans audit |
| **Modifier** un montant | Solde recalculé + enregistrement UPDATE dans audit |
| **Supprimer** un retrait | Montant remboursé + enregistrement DELETE dans audit |

### Formule du solde
```
Nouveau solde = Ancien solde + Montant_ancien - Montant_nouveau
```

---

## 🔧 API REST (Backend Flask)

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /api/clients | Liste des clients |
| GET | /api/retraits | Liste des retraits |
| POST | /api/retraits | Créer un retrait |
| PUT | /api/retraits/:id | Modifier un retrait |
| DELETE | /api/retraits/:id | Supprimer un retrait |
| GET | /api/audit | Journal d'audit + statistiques |
| GET | /api/health | Vérifier la connexion |

---

## ❗ Problèmes Courants

**"Cannot connect to database"**
→ Vérifier que Laragon est démarré et MySQL tourne sur le port 3306

**"Module not found"**
→ Relancer `pip install -r requirements.txt`

**Erreur CORS**
→ Le proxy Vite redirige `/api` vers Flask automatiquement. Ne pas appeler `localhost:5000` directement depuis le navigateur.

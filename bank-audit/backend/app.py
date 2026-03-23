"""
Backend Flask - Système d'Audit des Retraits Bancaires
Lancer: python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================
# CONFIGURATION BASE DE DONNÉES (Laragon)
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'bank_audit',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise Exception(f"Erreur connexion DB: {e}")


# ============================================
# ROUTES CLIENT — CRUD COMPLET
# ============================================

@app.route('/api/clients', methods=['GET'])
def get_clients():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM client ORDER BY nomclient")
    clients = cursor.fetchall()
    for c in clients:
        c['solde'] = float(c['solde'])
    cursor.close()
    conn.close()
    return jsonify(clients)


@app.route('/api/clients/<n_compte>', methods=['GET'])
def get_client(n_compte):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM client WHERE n_compte = %s", (n_compte,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()
    if not client:
        return jsonify({'error': 'Client non trouvé'}), 404
    client['solde'] = float(client['solde'])
    return jsonify(client)


@app.route('/api/clients', methods=['POST'])
def create_client():
    """Créer un nouveau client."""
    data = request.json
    required = ['n_compte', 'nomclient', 'solde']
    if not all(k in data for k in required):
        return jsonify({'error': 'Champs requis: n_compte, nomclient, solde'}), 400

    n_compte  = str(data['n_compte']).strip()
    nomclient = str(data['nomclient']).strip()
    solde     = data['solde']

    if not n_compte:
        return jsonify({'error': 'Le numéro de compte ne peut pas être vide'}), 400
    if not nomclient:
        return jsonify({'error': 'Le nom du client ne peut pas être vide'}), 400
    if len(n_compte) > 20:
        return jsonify({'error': 'N° compte trop long (max 20 caractères)'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Vérifier doublon
    cursor.execute("SELECT n_compte FROM client WHERE n_compte = %s", (n_compte,))
    if cursor.fetchone():
        cursor.close(); conn.close()
        return jsonify({'error': f"Le compte '{n_compte}' existe déjà"}), 409

    cursor.execute(
        "INSERT INTO client (n_compte, nomclient, solde) VALUES (%s, %s, %s)",
        (n_compte, nomclient, solde)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client créé avec succès', 'n_compte': n_compte}), 201


@app.route('/api/clients/<n_compte>', methods=['PUT'])
def update_client(n_compte):
    """Modifier le nom et/ou le solde d'un client."""
    data = request.json

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM client WHERE n_compte = %s", (n_compte,))
    client = cursor.fetchone()
    if not client:
        cursor.close(); conn.close()
        return jsonify({'error': 'Client non trouvé'}), 404

    # Champs modifiables : nomclient, solde
    nomclient = data.get('nomclient', client['nomclient'])
    solde     = data.get('solde',     client['solde'])

    if not str(nomclient).strip():
        cursor.close(); conn.close()
        return jsonify({'error': 'Le nom du client ne peut pas être vide'}), 400

    cursor.execute(
        "UPDATE client SET nomclient = %s, solde = %s WHERE n_compte = %s",
        (nomclient, solde, n_compte)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client mis à jour avec succès'})


@app.route('/api/clients/<n_compte>', methods=['DELETE'])
def delete_client(n_compte):
    """Supprimer un client (et ses retraits en cascade si FK CASCADE configurée)."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM client WHERE n_compte = %s", (n_compte,))
    if not cursor.fetchone():
        cursor.close(); conn.close()
        return jsonify({'error': 'Client non trouvé'}), 404

    # Supprimer les retraits liés d'abord (si pas de CASCADE en DB)
    cursor.execute("DELETE FROM retrait WHERE n_compte = %s", (n_compte,))
    cursor.execute("DELETE FROM client WHERE n_compte = %s", (n_compte,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client supprimé avec succès'})


# ============================================
# ROUTES RETRAIT (CRUD)
# ============================================

@app.route('/api/retraits', methods=['GET'])
def get_retraits():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, c.nomclient, c.solde 
        FROM retrait r 
        JOIN client c ON r.n_compte = c.n_compte
        ORDER BY r.n_retrait DESC
    """)
    retraits = cursor.fetchall()
    for r in retraits:
        r['montant'] = float(r['montant'])
        r['solde']   = float(r['solde'])
    cursor.close()
    conn.close()
    return jsonify(retraits)


@app.route('/api/retraits', methods=['POST'])
def create_retrait():
    data = request.json
    required = ['n_cheque', 'n_compte', 'montant']
    if not all(k in data for k in required):
        return jsonify({'error': 'Champs manquants: n_cheque, n_compte, montant'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM client WHERE n_compte = %s", (data['n_compte'],))
    client = cursor.fetchone()
    if not client:
        cursor.close(); conn.close()
        return jsonify({'error': 'Compte client inexistant'}), 404
    if float(client['solde']) < float(data['montant']):
        cursor.close(); conn.close()
        return jsonify({'error': f"Solde insuffisant. Solde actuel: {client['solde']}"}), 400

    cursor.execute(
        "INSERT INTO retrait (n_cheque, n_compte, montant) VALUES (%s, %s, %s)",
        (data['n_cheque'], data['n_compte'], data['montant'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'message': 'Retrait créé avec succès', 'n_retrait': new_id}), 201


@app.route('/api/retraits/<int:n_retrait>', methods=['PUT'])
def update_retrait(n_retrait):
    data = request.json
    if 'montant' not in data:
        return jsonify({'error': 'Champ montant requis'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT r.*, c.solde FROM retrait r JOIN client c ON r.n_compte = c.n_compte WHERE r.n_retrait = %s",
        (n_retrait,)
    )
    retrait = cursor.fetchone()
    if not retrait:
        cursor.close(); conn.close()
        return jsonify({'error': 'Retrait non trouvé'}), 404

    diff = float(data['montant']) - float(retrait['montant'])
    if diff > 0 and float(retrait['solde']) < diff:
        cursor.close(); conn.close()
        return jsonify({'error': 'Solde insuffisant pour la mise à jour'}), 400

    cursor.execute(
        "UPDATE retrait SET montant = %s WHERE n_retrait = %s",
        (data['montant'], n_retrait)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Retrait mis à jour avec succès'})


@app.route('/api/retraits/<int:n_retrait>', methods=['DELETE'])
def delete_retrait(n_retrait):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT n_retrait FROM retrait WHERE n_retrait = %s", (n_retrait,))
    if not cursor.fetchone():
        cursor.close(); conn.close()
        return jsonify({'error': 'Retrait non trouvé'}), 404

    cursor.execute("DELETE FROM retrait WHERE n_retrait = %s", (n_retrait,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Retrait supprimé avec succès'})


# ============================================
# ROUTE AUDIT
# ============================================

@app.route('/api/audit', methods=['GET'])
def get_audit():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM audit_retrait ORDER BY date_maj DESC")
    audits = cursor.fetchall()

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN type_action = 'INSERT' THEN 1 ELSE 0 END) as nb_insertions,
            SUM(CASE WHEN type_action = 'UPDATE' THEN 1 ELSE 0 END) as nb_modifications,
            SUM(CASE WHEN type_action = 'DELETE' THEN 1 ELSE 0 END) as nb_suppressions
        FROM audit_retrait
    """)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    for a in audits:
        if isinstance(a['date_maj'], datetime):
            a['date_maj'] = a['date_maj'].strftime('%Y-%m-%d %H:%M:%S')
        if a['montant_ancien'] is not None:
            a['montant_ancien'] = float(a['montant_ancien'])
        if a['montant_nouv'] is not None:
            a['montant_nouv'] = float(a['montant_nouv'])

    return jsonify({
        'audit': audits,
        'stats': {
            'nb_insertions':    int(stats['nb_insertions']    or 0),
            'nb_modifications': int(stats['nb_modifications'] or 0),
            'nb_suppressions':  int(stats['nb_suppressions']  or 0)
        }
    })


# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({'status': 'OK', 'database': 'Connecté'})
    except Exception as e:
        return jsonify({'status': 'ERROR', 'database': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Serveur Flask démarré sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
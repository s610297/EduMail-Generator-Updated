from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
import random
import string
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'mailbox.db')

# Default custom domain
CUSTOM_DOMAIN = os.getenv('MAIL_DOMAIN', 'local.test')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inboxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alias TEXT NOT NULL UNIQUE,
            domain TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inbox_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(inbox_id) REFERENCES inboxes(id)
        )
    ''')
    conn.commit()
    conn.close()


def generate_alias(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def get_inbox_email(alias, domain=None):
    if domain is None:
        domain = CUSTOM_DOMAIN
    return f"{alias}@{domain}"


def add_message(inbox_id, sender, subject, body):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (inbox_id, sender, subject, body, created_at) VALUES (?, ?, ?, ?, ?)',
        (inbox_id, sender, subject, body, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    inboxes = conn.execute('SELECT * FROM inboxes ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', inboxes=inboxes, custom_domain=CUSTOM_DOMAIN)


@app.route('/api/config')
def get_config():
    return jsonify({'domain': CUSTOM_DOMAIN})


@app.route('/api/inbox', methods=['POST'])
def create_inbox():
    data = request.get_json(silent=True) or {}
    alias = (data.get('alias') or generate_alias()).strip().lower()
    domain = (data.get('domain') or CUSTOM_DOMAIN).strip().lower()
    
    if not alias:
        alias = generate_alias()
    if not domain:
        domain = CUSTOM_DOMAIN

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO inboxes (alias, domain, created_at) VALUES (?, ?, ?)',
            (alias, domain, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        inbox_id = conn.execute('SELECT id FROM inboxes WHERE alias = ? AND domain = ?', (alias, domain)).fetchone()['id']
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'This email already exists. Try another alias or domain.'}), 400

    conn.close()
    email = get_inbox_email(alias, domain)
    return jsonify({'id': inbox_id, 'alias': alias, 'domain': domain, 'email': email}), 201


@app.route('/api/inboxes')
def list_inboxes():
    conn = get_db_connection()
    inboxes = conn.execute('SELECT * FROM inboxes ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([{
        'id': row['id'],
        'alias': row['alias'],
        'domain': row['domain'],
        'email': get_inbox_email(row['alias'], row['domain']),
        'created_at': row['created_at']
    } for row in inboxes])


@app.route('/api/inbox/<int:inbox_id>')
def get_inbox_messages(inbox_id):
    conn = get_db_connection()
    inbox = conn.execute('SELECT * FROM inboxes WHERE id = ?', (inbox_id,)).fetchone()
    if not inbox:
        conn.close()
        return jsonify({'error': 'Inbox not found'}), 404

    messages = conn.execute(
        'SELECT * FROM messages WHERE inbox_id = ? ORDER BY id DESC',
        (inbox_id,)
    ).fetchall()

    result = {
        'id': inbox['id'],
        'alias': inbox['alias'],
        'domain': inbox['domain'],
        'email': get_inbox_email(inbox['alias'], inbox['domain']),
        'messages': [
            {
                'id': m['id'],
                'sender': m['sender'],
                'subject': m['subject'],
                'body': m['body'],
                'created_at': m['created_at']
            }
            for m in messages
        ]
    }
    conn.close()
    return jsonify(result)


@app.route('/api/send-otp/<int:inbox_id>', methods=['POST'])
def send_otp(inbox_id):
    conn = get_db_connection()
    inbox = conn.execute('SELECT * FROM inboxes WHERE id = ?', (inbox_id,)).fetchone()
    conn.close()

    if not inbox:
        return jsonify({'error': 'Inbox not found'}), 404

    otp = ''.join(random.choice(string.digits) for _ in range(6))
    body = f"Your activation code is: {otp}\nThis is a local sandbox OTP demo."
    add_message(inbox_id, 'system@' + inbox['domain'], 'Activation Code', body)
    return jsonify({'otp': otp, 'email': get_inbox_email(inbox['alias'], inbox['domain'])})


@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json(silent=True) or {}
    inbox_id = data.get('inbox_id')
    sender = data.get('sender', 'demo@local.test')
    subject = data.get('subject', 'Test Message')
    body = data.get('body', 'This is a local sandbox message.')

    if not inbox_id:
        return jsonify({'error': 'inbox_id is required'}), 400

    conn = get_db_connection()
    inbox = conn.execute('SELECT * FROM inboxes WHERE id = ?', (inbox_id,)).fetchone()
    conn.close()

    if not inbox:
        return jsonify({'error': 'Inbox not found'}), 404

    add_message(inbox_id, sender, subject, body)
    return jsonify({'success': True})


@app.route('/delete-inbox/<int:inbox_id>', methods=['POST'])
def delete_inbox(inbox_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE inbox_id = ?', (inbox_id,))
    conn.execute('DELETE FROM inboxes WHERE id = ?', (inbox_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

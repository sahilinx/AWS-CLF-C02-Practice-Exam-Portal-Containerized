from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'examdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'secret')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS exam_results (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100),
            student_name VARCHAR(200),
            batch VARCHAR(100),
            score INTEGER,
            total_questions INTEGER,
            percentage INTEGER,
            passed BOOLEAN,
            exam_start_time VARCHAR(50),
            exam_end_time VARCHAR(50),
            date VARCHAR(20),
            time_elapsed INTEGER,
            exam_type VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/exam-results', methods=['POST', 'OPTIONS'])
def save_result():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    try:
        body = request.get_json()

        now = datetime.now(timezone.utc).isoformat()
        body['examEndTime'] = now
        body['examStartTime'] = now
        body['date'] = now.split('T')[0]

        init_db()
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO exam_results (
                session_id, student_name, batch, score,
                total_questions, percentage, passed,
                exam_start_time, exam_end_time, date,
                time_elapsed, exam_type
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            body.get('sessionId'),
            body.get('studentName'),
            body.get('batch'),
            body.get('score'),
            body.get('totalQuestions'),
            body.get('percentage'),
            body.get('passed'),
            body.get('examStartTime'),
            body.get('examEndTime'),
            body.get('date'),
            body.get('timeElapsed'),
            body.get('examType')
        ))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    try:
        init_db()
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # get filter params from URL
        name    = request.args.get('name')
        batch   = request.args.get('batch')
        passed  = request.args.get('passed')
        date    = request.args.get('date')

        query  = 'SELECT * FROM exam_results WHERE 1=1'
        params = []

        if name:
            query += ' AND LOWER(student_name) LIKE LOWER(%s)'
            params.append(f'%{name}%')
        if batch:
            query += ' AND LOWER(batch) LIKE LOWER(%s)'
            params.append(f'%{batch}%')
        if passed is not None:
            query += ' AND passed = %s'
            params.append(passed.lower() == 'true')
        if date:
            query += ' AND date = %s'
            params.append(date)

        query += ' ORDER BY created_at DESC'

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'results': list(rows)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

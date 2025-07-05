import uuid
import threading
import subprocess
from flask import Flask, request, jsonify
from github_username import extract_company_github_username
from git_org_data import get_org_public_members
from database import init_db, save_job

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        job_id = str(uuid.uuid4())
        filename = file.filename

        try:
            username = extract_company_github_username(file.stream)
            public_members = get_org_public_members(username)
            member_usernames = [member["login"] for member in public_members]

            save_job(
                job_id=job_id,
                filename=filename,
                company_name=username,
                github_members=member_usernames,
                status="success"
            )

            return jsonify({
                "job_id": job_id,
                "github_username": username,
                "public_members": member_usernames
            }), 200

        except Exception as e:
            save_job(
                job_id=job_id,
                filename=filename,
                company_name=None,
                github_members=None,
                status="failure"
            )

            return jsonify({
                "job_id": job_id,
                "error": str(e)
            }), 500

    return jsonify({"error": "Only PDF files are allowed"}), 400

def run_flask():
    app.run(debug=False, use_reloader=False)

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "ui.py"])

if __name__ == '__main__':
    init_db()
    threading.Thread(target=run_flask).start()
    run_streamlit()
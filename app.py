import uuid
from flask import Flask, request, jsonify
from github_username import extract_company_github_username

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
        try:
            username = extract_company_github_username(file.stream)
            return jsonify({
                "job_id": job_id,
                "github_username": username
            }), 200
        except Exception as e:
            return jsonify({
                "job_id": job_id,
                "error": str(e)
            }), 500
    else:
        return jsonify({"error": "Only PDF files are allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "secure123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- LOGIN ----------
@app.route('/')
def home():
    return redirect(url_for('dashboard'))



# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():


    from datetime import datetime
    import os

    files = []

    for filename in os.listdir(UPLOAD_FOLDER):

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        extension = filename.split('.')[-1].lower()

        if extension in ['exe', 'bat', 'vbs', 'ps1', 'js']:
            status = "Unsafe"
        else:
            status = "Safe"

        upload_time = datetime.fromtimestamp(
        os.path.getmtime(filepath)
        ).strftime("%d-%m-%Y %H:%M")


        files.append({
            "name": filename,
            "status": status,
            "time": upload_time
        })

    # ⭐ ADD THIS PART (NEW)
    total_files = len(files)
    safe_files = len([f for f in files if f["status"] == "Safe"])
    unsafe_files = len([f for f in files if f["status"] == "Unsafe"])

    user = "Admin"

    return render_template(
        "dashboard.html",
        files=files,
        total_files=total_files,
        safe_files=safe_files,
        unsafe_files=unsafe_files,
        user=user
    )

# ---------- FILE UPLOAD ----------
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']
    if file and file.filename != "":
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

    return redirect(url_for('dashboard'))


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return "File not found"

    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )
@app.route('/delete/<filename>')
def delete(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run()


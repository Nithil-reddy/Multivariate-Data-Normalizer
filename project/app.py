from flask import Flask, render_template, request, send_file
import pandas as pd
import os

# Create Flask app
app = Flask(__name__)

# Folders for uploaded and output files
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # make folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1. Get uploaded file from form
        file = request.files["file"]

        # If no file was uploaded
        if file.filename == "":
            return "⚠️ No file selected!"

        # 2. Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 3. Read CSV into pandas DataFrame
        df = pd.read_csv(filepath)

        # 4. Normalize data using min-max formula
        normalized_df = (df - df.min()) / (df.max() - df.min())

        # 5. Save normalized file
        output_file = os.path.join(OUTPUT_FOLDER, "normalized_" + file.filename)
        normalized_df.to_csv(output_file, index=False)

        # 6. Show preview (first 5 rows) in result.html
        return render_template(
        "result.html",
        tables=normalized_df.head().to_html(classes="data", index=False),
        filename="normalized_" + file.filename
)

   


    # If GET request → show upload page
    return render_template("index.html")


# ---------------- DOWNLOAD ROUTE ----------------
@app.route("/download/<filename>")
def download(filename):
    """Allow user to download the normalized CSV file"""
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

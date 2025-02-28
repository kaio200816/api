from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")  # Pasta para salvar os vídeos
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Cria a pasta se não existir

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Nenhuma URL fornecida"}), 400

    output_path = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")  # Nome do arquivo
    command = ["yt-dlp", "-o", output_path, "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]", video_url]

    try:
        subprocess.run(command, check=True)
        return jsonify({"message": "Download iniciado com sucesso!", "path": DOWNLOAD_FOLDER})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Erro ao baixar o vídeo"}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))  # Pega a porta do ambiente da Render
    app.run(host="0.0.0.0", port=PORT, debug=True)

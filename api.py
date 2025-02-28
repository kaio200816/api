from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")  # Pasta para salvar os vídeos
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Cria a pasta se não existir

@app.route('/')
def home():
    return "API de download de vídeo está funcionando. Use o endpoint /download para baixar vídeos."

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Nenhuma URL fornecida"}), 400

    # Caminho onde o vídeo será salvo
    output_path = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")

    # Comando para o yt-dlp
    command = ["yt-dlp", "-o", output_path, "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]", video_url]

    try:
        # Verifica se o yt-dlp está instalado corretamente
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Executa o comando para baixar o vídeo
        subprocess.run(command, check=True)
        
        # Após o download, buscamos o nome do arquivo
        file_name = get_downloaded_file(output_path)

        if file_name:
            # Retorna o link para o arquivo
            download_link = f"/download/{file_name}"
            return jsonify({"message": "Download iniciado com sucesso!", "download_link": download_link})
        else:
            return jsonify({"error": "Não foi possível encontrar o arquivo após o download."}), 500

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Erro ao baixar o vídeo", "details": str(e)}), 500
    except FileNotFoundError:
        return jsonify({"error": "yt-dlp não encontrado. Por favor, instale o yt-dlp."}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

def get_downloaded_file(output_path):
    # Procurar na pasta de downloads o arquivo gerado pelo yt-dlp
    for file in os.listdir(DOWNLOAD_FOLDER):
        if file.endswith(".mp4"):  # Procuramos apenas arquivos MP4
            return file
    return None

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))  # Pega a porta do ambiente da Render
    app.run(host="0.0.0.0", port=PORT, debug=True)

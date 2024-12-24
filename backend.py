from flask import Flask, request, jsonify, CORS
import yt_dlp as youtube_dl
import re
import os

app = Flask(__name__)
CORS(app)  # Configuración para permitir CORS

DOWNLOAD_FOLDER = "videos_descargados"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def limpiar_url(url):
    return re.sub(r'&list=[^&]+', '', url)

def es_url_valida(url):
    patron = r'^https?://(www\.)?(youtube\.com|youtu\.be)/.+$'
    return re.match(patron, url)

@app.route('/download', methods=['POST'])
def descargar_video():
    data = request.json
    url = data.get("url")
    if not url or not es_url_valida(url):
        return jsonify({"error": "URL no válida"}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }
    try:
        url = limpiar_url(url)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return jsonify({
                "message": "Descarga completa",
                "title": info.get('title', 'Video'),
                "file_path": os.path.join(DOWNLOAD_FOLDER, f"{info.get('title', 'Video')}.{info.get('ext', 'mp4')}")
            }), 200
    except youtube_dl.utils.DownloadError as e:
        return jsonify({"error": "Error al descargar el video: {}".format(str(e))}), 500
    except youtube_dl.utils.ExtractorError as e:
        return jsonify({"error": "Error del extractor: {}".format(str(e))}), 500
    except Exception as e:
        return jsonify({"error": "Error inesperado: {}".format(str(e))}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
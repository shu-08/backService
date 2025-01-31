from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# 動画の保存先
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # ここはそのままHTMLを返します

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']  # フロントエンドから送られたURLを取得
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_info['title']}.{video_info['ext']}")
        
        # 成功時にJSON形式でダウンロードリンクを返す
        return jsonify({'download_link': file_path})
    
    except Exception as e:
        # エラーが発生した場合もJSON形式でエラーメッセージを返す
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

def get_playlist_data(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download videos, just metadata
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    playlist_title = info['title']
    video_titles = [entry['title'] for entry in info['entries']]
    video_views = [entry['view_count'] for entry in info['entries']]

    return {
        'title': playlist_title,
        'videos': video_titles,
        'views': video_views
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    playlist_url = request.form['playlist_url']
    
    if playlist_url:
        data = get_playlist_data(playlist_url)
        return render_template('result.html', data=data)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

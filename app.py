from flask import Flask, render_template, abort, send_from_directory
import os
import markdown

app = Flask(__name__)
app.config['MD_FOLDER'] = 'md_files'

def get_file_content(filename):
    try:
        with open(os.path.join(app.config['MD_FOLDER'], filename), 'r', encoding='utf-8') as file:
            return file.read()
    except IOError:
        return None

@app.route('/')
def index():
    files = os.listdir(app.config['MD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/view/<filename>')
def view_file(filename):
    if not filename.endswith(('.md', '.mdx')):
        abort(404)
    else:
        content = get_file_content(filename)
        if content is None:
            abort(404)
        rendered_content = markdown.markdown(content)
    
    return render_template('view.html', content=rendered_content, filename=filename)

@app.route('/md_files/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['MD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

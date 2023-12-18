from flask import Flask, request, jsonify, send_file,abort
from flask_cors import CORS
import psutil
import os
import encoder
import decoder
import shutil
import io
import mimetypes

app = Flask(__name__)
CORS(app)

def human_readable_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB" 


@app.route('/list-files')
def list_files():
    root_dir = r'/home/exarilo/Documents/Root'
    return jsonify(walk_dir(root_dir))

def walk_dir(dir_path):
    dir_name = os.path.basename(dir_path)
    if os.path.isdir(dir_path):
        directories = []
        files = []
        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)
            if os.path.isdir(full_path):
                directories.append(walk_dir(full_path))
            else:
                files.append({
                    "type": "file",
                    "name": name,
                    "full_path": full_path
                })
        return {
            "type": "directory",
            "name": dir_name,
            "directories": directories,
            "files": files
        }
    else:
        return {
            "type": "file",
            "name": dir_name,
            "full_path": dir_path
        }

@app.route('/disk-space')
def disk_space():
    disk_info = psutil.disk_usage('/')
    total_space = human_readable_size(disk_info.total)
    used_space = human_readable_size(disk_info.used)
    free_space = human_readable_size(disk_info.free)
    return jsonify({'total_space': total_space,
                    'used_space': used_space,
                    'free_space': free_space})



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    folderDestination = request.form['folderDest']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try: 
        file_bytes_input = file.read()
        filename = file.filename
        #filename = os.path.basename(args.path)
        bitmap_output = encoder.to_bitmap(file_bytes_input, filename)
        output_image_path = os.path.join(r'/home/exarilo/Documents/',folderDestination, filename + '.png')
        bitmap_output.save(output_image_path)

    except IOError as e:
        raise Exception(f"Error: {e}")

    return jsonify({'message': 'File uploaded successfully'})

@app.route('/delete', methods=['DELETE'])
def delete_file():
    path = r'/home/exarilo/Documents/'+request.args.get('path').replace('\\', '/')
    print(path)

    if not path:
        return jsonify({'error': 'No path specified'}), 400  

    try:
        if path.endswith("Root"):
            return jsonify({'error': 'Root folder could not be deleted'}), 403 
        
        path = os.path.join(r'/home/exarilo/Documents/Root', path)

        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
                return jsonify({'message': f'{path} deleted successfully'})
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return jsonify({'message': f'{path} deleted successfully'})
            else:
                return jsonify({'error': 'Path is neither a file nor a directory'}), 400 
        else:
            return jsonify({'error': 'Path does not exist'}), 404  
    except Exception as e:
        return jsonify({'error': f'Error deleting {path}: {e}'}), 500 


@app.route('/download', methods=['GET'])
def download_file():
    path = request.args.get('path')

    if not path:
        return jsonify({'error': 'No path specified'})

    full_path = os.path.join(r'/home/exarilo/Documents/', path).replace('\\', '/')

    try:
        print(full_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            _, ext = os.path.splitext(full_path)
            if ext.lower() == '.png':
                filename, image_data = decoder.decode_image(full_path)
                mimetype = mimetypes.types_map.get(ext.lower(), 'application/octet-stream')
                return send_file(io.BytesIO(image_data), mimetype=mimetype, as_attachment=True, attachment_filename=filename)
            else:
                return send_file(full_path, as_attachment=True)
        else:
            abort(404, description='File does not exist or is not a file')
    except Exception as e:
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        abort(500, description=f'Error during download: {e}')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

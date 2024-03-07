from flask import Flask, jsonify, request, render_template, send_from_directory
from UITasks import long_running_task
import os
import time


app = Flask(__name__)
task_in_progress = False


@app.route('/', methods=['GET'])
def index():
    # Display the upload form
    return render_template('index.html')

@app.route('/get_folders/<option>')
def get_folders(option):
    base_path = 'assets'
    if option == 'distortNew':
        folder_path = os.path.join(base_path, 'distortNew')
    else:
        folder_path = os.path.join(base_path, 'distorted')
    
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return jsonify(folders)
    
@app.route('/process-all', methods=['POST'])
def process_all():
    global task_in_progress
    data = request.json
    # Process your data here. For example:
    print(data)
    task_in_progress = True
    long_running_task(data)
    # Return a response, such as confirmation of processing
    print("FINISHED")
    task_in_progress = False
    return jsonify({"status": "success", "message": "Data processed"})

@app.route('/get-common-subfolders', methods=['POST'])
def get_common_subfolders():
    data = request.json
    selected_folders = data['selectedFolders']
    base_path = "assets/distorted"
    
    # A set to store common subfolders
    common_subfolders = None
    for folder in selected_folders:
        current_path = os.path.join(base_path, folder)
        current_subfolders = {f.name for f in os.scandir(current_path) if f.is_dir()}

        if common_subfolders is None:
            common_subfolders = current_subfolders
        else:
            common_subfolders &= current_subfolders
    if selected_folders:
        return jsonify(list(common_subfolders))
    else:
        return jsonify({"status": "success", "message": "No data"})

@app.route('/check-task-status')
def check_task_status():
    global task_in_progress
    # Logic to determine if a task is in progress
    # This might check a database, in-memory data structure, or other indicators
    # Example: Replace with actual check

    return jsonify({'taskInProgress': task_in_progress})

@app.route('/wait-for-task-completion')
def wait_for_task_completion():
    global task_in_progress
    while task_in_progress:
        time.sleep(1)
    return jsonify({'status': 'completed'})

if __name__ == '__main__':
    app.run(debug=True, port=7865)

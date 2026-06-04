from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
import os
from amazon import main

app = Flask(__name__)

def filechecker(old_list, new_list):
    """Return items that appear in new_list but not in old_list."""
    return [i for i in new_list if i not in old_list]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('product_url', '').strip()
        if url:
            # snapshot of directories before running
            cluster_before = os.listdir('Cluster') if os.path.isdir('Cluster') else []
            attribute_before = os.listdir('Attribute') if os.path.isdir('Attribute') else []
            output_before = os.listdir('Data_Output') if os.path.isdir('Data_Output') else []
            images_before = os.listdir('image_data_store') if os.path.isdir('image_data_store') else []

            result = main(url)

            cluster_after = os.listdir('Cluster') if os.path.isdir('Cluster') else []
            attribute_after = os.listdir('Attribute') if os.path.isdir('Attribute') else []
            output_after = os.listdir('Data_Output') if os.path.isdir('Data_Output') else []
            images_after = os.listdir('image_data_store') if os.path.isdir('image_data_store') else []

            new_cluster = filechecker(cluster_before, cluster_after)
            new_attribute = filechecker(attribute_before, attribute_after)
            new_output = filechecker(output_before, output_after)
            new_images = filechecker(images_before, images_after)

            return render_template(
                'results.html',
                result=result,
                cluster=new_cluster,
                attribute=new_attribute,
                output=new_output,
                images=new_images,
            )
    return render_template('index.html')


@app.route('/download/<path:folder>/<filename>')
def download(folder, filename):
    # only allow access to expected directories
    safe_folders = ['Cluster', 'Attribute', 'Data_Output', 'image_data_store']
    if folder not in safe_folders:
        abort(404)
    return send_from_directory(folder, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

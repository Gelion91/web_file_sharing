import os
from fileinput import filename
from flask import Blueprint, render_template, flash, url_for, request, current_app
from werkzeug.utils import redirect, secure_filename


from main.forms import UploadForm

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():
    title = 'Главная страница'
    return render_template('start.html', page_title=title)


@blueprint.route('/upload')
def upload():
    title = 'Добавить'
    upload_form = UploadForm()
    return render_template('upload/upload.html', page_title=title, form=upload_form)


@blueprint.route('/process_upload', methods=['POST'])
def process_upload():
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        if request.method == 'POST':
            f = upload_form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(current_app.instance_path, filename[:2], filename
            ))
        flash('Файл сохранен')
        flash(f'хэш-ключ:')
        return redirect(url_for('main.upload'))

    flash('Файл не выбран.')
    return redirect(url_for('main.upload'))


@blueprint.route('/download')
def download():
    title = 'Скачать'


@blueprint.route('/delete')
def delete():
    title = 'Удалить'

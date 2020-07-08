import os
from flask import Blueprint, render_template, flash, url_for, request
from werkzeug.utils import redirect, secure_filename
from main.forms import UploadForm

blueprint = Blueprint('main', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))


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
    """ Добавление файла """
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        if request.method == 'POST':
            f = upload_form.file.data
            filename = secure_filename(f.filename)
            filename = str(hash(filename))
            if not os.path.exists(os.path.join(basedir, '..', 'store')):
                os.mkdir(os.path.join(basedir, '..', 'store'))
            os.mkdir(os.path.join(basedir, '..', 'store', filename[:2]))
            f.save(os.path.join(basedir, '..', 'store', filename[:2], filename))

        flash('Файл сохранен')
        flash(f'хэш-ключ: {filename}')
        return redirect(url_for('main.upload'))

    flash('Файл не выбран.')
    return redirect(url_for('main.upload'))


@blueprint.route('/download')
def download():
    title = 'Скачать'


@blueprint.route('/delete')
def delete():
    title = 'Удалить'

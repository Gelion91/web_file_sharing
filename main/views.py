import hashlib
import os
from flask import Blueprint, render_template, flash, url_for, request, send_file, current_app
from werkzeug.utils import redirect
from main.forms import UploadForm, DownloadForm, DeleteForm
from .utils import get_hash

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/upload')
def upload():
    title = 'Добавить файл на сервер'
    upload_form = UploadForm()
    return render_template('upload/upload.html', page_title=title, form=upload_form)


@blueprint.route('/process_upload', methods=['POST'])
def process_upload():
    """ Добавление файла на сервер """
    upload_form = UploadForm()

    if not upload_form.validate_on_submit():
        flash('Файл не выбран.')
        return redirect(url_for('main.upload'))

    f = upload_form.file.data
    result = get_hash(f)
    if not os.path.exists(os.path.join(current_app.config['PATH'], result[:2])):
        os.makedirs(os.path.join(current_app.config['PATH'], result[:2]))
    f.save(os.path.join(current_app.config['PATH'], result[:2], result))
    f.seek(0)
    with open(os.path.join(current_app.config['PATH'], result[:2], result), 'wb') as fl:
        fl.write(f.read())
        fl.close()
        flash('Файл сохранен')
        flash(f'хэш: {result}')
    return redirect(url_for('main.upload'))


@blueprint.route('/download')
def download():
    title = 'Скачать файл'
    download_form = DownloadForm()
    return render_template('download/download.html', page_title=title, form=download_form)


@blueprint.route('/process_download', methods=['GET', 'POST'])
def process_download():
    """ Скачать файл с сервера """
    download_form = DownloadForm()
    if not download_form.validate_on_submit():
        flash('Введите хэш.')
        return redirect(url_for('main.download'))

    if not request.method == 'POST':
        return redirect(url_for('main.upload'))

    result = download_form.file.data
    try:
        return send_file(os.path.join(current_app.config['PATH'], result[:2], result), as_attachment=True)
    except FileNotFoundError:
        flash('Файл не найден.')
        return redirect(url_for('main.download'))


@blueprint.route('/delete')
def delete():
    title = 'Удалить файл'
    delete_form = DeleteForm()
    return render_template('delete/delete.html', page_title=title, form=delete_form)


@blueprint.route('/process_delete', methods=['GET', 'POST'])
def process_delete():
    """ Удаление файла с сервера """
    delete_form = DeleteForm()
    if not delete_form.validate_on_submit():
        flash('Введите хэш.')
        return redirect(url_for('main.delete'))

    if not request.method == 'POST':
        return redirect(url_for('main.delete'))

    result = delete_form.file.data
    try:
        os.remove(os.path.join(current_app.config['PATH'], result[:2], result))
        if not os.listdir(os.path.join(current_app.config['PATH'], result[:2])):
            os.rmdir(os.path.join(current_app.config['PATH'], result[:2]))
        flash('Файл успешно удален.')
        return redirect(url_for('main.delete'))
    except FileNotFoundError:
        flash('Файл не найден.')
        return redirect(url_for('main.delete'))

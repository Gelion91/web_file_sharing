import os
from glob import glob

from flask import Blueprint, render_template, flash, url_for, request, send_file
from werkzeug.utils import redirect, secure_filename
from main.forms import UploadForm, DownloadForm, DeleteForm

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
    """ Добавить файл """
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        if request.method == 'POST':
            f = upload_form.file.data
            filename = secure_filename(f.filename)
            filename = str(hash(filename))
            if not os.path.exists(os.path.join(basedir, '..', 'store')):
                os.mkdir(os.path.join(basedir, '..', 'store'))
            if not os.path.exists(os.path.join(basedir, '..', 'store', filename[:2])):
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
    download_form = DownloadForm()
    return render_template('download/download.html', page_title=title, form=download_form)


@blueprint.route('/process_download', methods=['GET', 'POST'])
def process_download():
    """ Скачать файл """
    download_form = DownloadForm()
    if download_form.validate_on_submit():
        if request.method == 'POST':
            result = download_form.file.data
            try:
                return send_file(os.path.join(basedir, '..', 'store', result[:2], result), as_attachment=True)
            except FileNotFoundError:
                flash('Файл не найден.')
                return redirect(url_for('main.download'))

    flash('Введите ключ.')
    return redirect(url_for('main.download'))


@blueprint.route('/delete')
def delete():
    title = 'Удалить'
    delete_form = DeleteForm()
    return render_template('delete/delete.html', page_title=title, form=delete_form)


@blueprint.route('/process_delete', methods=['GET', 'POST'])
def process_delete():
    """ Удаление файла """
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        if request.method == 'POST':
            result = delete_form.file.data
            try:
                os.remove(os.path.join(basedir, '..', 'store', result[:2], result))
                flash('Файл успешно удален.')
                return redirect(url_for('main.delete'))
            except FileNotFoundError:
                flash('Файл не найден.')
                return redirect(url_for('main.delete'))

    flash('Введите ключ.')
    return redirect(url_for('main.delete'))

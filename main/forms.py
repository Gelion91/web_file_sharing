from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField('Файл', validators=[DataRequired()], render_kw={'class': 'form-control-file'})
    submit = SubmitField('Добавить', render_kw={'class': 'btn btn-primary'})


class DownloadForm(FlaskForm):
    file = StringField('Хэш-ключ', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Скачать', render_kw={'class': 'btn btn-primary'})


class DeleteForm(FlaskForm):
    file = StringField('Хэш-ключ', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Удалить', render_kw={'class': 'btn btn-primary'})
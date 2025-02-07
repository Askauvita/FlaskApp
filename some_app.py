from flask import Flask, render_template, request
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageOps
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap

from forms import NetForm
from net import add_border, create_color_distribution

# Инициализация Flask-приложения
app = Flask(__name__)
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfdX84qAAAAAKAgxm6ezMiHXqhSrmVGCpNfMvgu'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfdX84qAAAAAEzSMg47UgQMX8no3MUD5BZ83qjr'
Bootstrap(app)


# Форма для добавления рамки
class BorderForm(FlaskForm):
    upload = FileField('Загрузите изображение', validators=[
        InputRequired(),
    ])
    recaptcha = RecaptchaField()
    border_size = IntegerField('Размер рамки (пикселей)', validators=[InputRequired()])
    submit = SubmitField('Добавить рамку')


@app.route("/", methods=['GET', 'POST'])
def index():
    form = BorderForm()
    if form.validate_on_submit():
        # Загружаем файл
        file = request.files['upload']
        if file:
            # Создаем безопасное имя файла
            filename = secure_filename(file.filename)
            filepath = os.path.join('./static', filename)

            # Сохраняем файл на диск
            file.save(filepath)

            # Добавляем рамку
            bordered_image = add_border(filepath, form.border_size.data)
            bordered_filepath = os.path.join('./static', 'bordered_' + filename)
            bordered_image.save(bordered_filepath)

            # Создаем график распределения цветов
            original_plot = create_color_distribution(filepath)
            bordered_plot = create_color_distribution(bordered_filepath)

            return render_template('net.html',
                                   form=form,
                                   original_image=filepath,
                                   bordered_image=bordered_filepath,
                                   original_plot=original_plot,
                                   bordered_plot=bordered_plot)

    return render_template('index.html', form=form)


# Функция сохранения графика в формате base64
def save_plot_to_base64(color_distribution):
    import matplotlib.pyplot as plt
    import base64
    from io import BytesIO
    plt.bar(['Red', 'Green', 'Blue'], color_distribution)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return image_base64


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

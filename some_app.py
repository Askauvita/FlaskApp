from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap

# Инициализация Flask-приложения
app = Flask(__name__)
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = 'YOUR_RECAPTCHA_PUBLIC_KEY'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'YOUR_RECAPTCHA_PRIVATE_KEY'
Bootstrap(app)

# Форма для добавления рамки
class BorderForm(FlaskForm):
    file = FileField('Загрузите изображение', validators=[InputRequired()])
    border_size = IntegerField('Размер рамки (пикселей)', validators=[InputRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Добавить рамку')

@app.route("/", methods=['GET', 'POST'])
def index():
    form = BorderForm()
    if form.validate_on_submit():
        # Обработка загруженного файла
        file = form.file.data
        border_size = form.border_size.data

        # Сохранение файла во временную директорию
        filename = os.path.join('static', secure_filename(file.filename))
        file.save(filename)

        # Добавление рамки
        from net import add_border, create_color_distribution
        bordered_image = add_border(filename, border_size)
        bordered_filename = os.path.join('static', 'bordered_' + secure_filename(file.filename))
        bordered_image.save(bordered_filename)

        # Генерация графика распределения цветов
        original_colors = create_color_distribution(Image.open(filename).convert('RGB'))
        original_plot = save_plot_to_base64(original_colors)

        return render_template('net.html',
                               form=form,
                               original_image=filename,
                               bordered_image=bordered_filename,
                               original_plot=original_plot)

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

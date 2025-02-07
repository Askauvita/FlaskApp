import requests
from io import BytesIO
import base64

# Путь к тестовому изображению
path = './static/image0008.png'

# Чтение файла и кодирование в base64
with open(path, 'rb') as fh:
    img_data = fh.read()
    b64 = base64.b64encode(img_data).decode('utf-8')

# JSON-запрос для передачи данных
jsondata = {'imagebin': b64, 'border_size': 50}
res = requests.post('http://localhost:5000/apinet', json=jsondata)

if res.ok:
    print(res.json())
else:
    print("Ошибка:", res.status_code)

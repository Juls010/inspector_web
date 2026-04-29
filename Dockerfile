# Usa una imagen oficial de Python ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y asegura que los logs salgan en consola en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea y establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código fuente del proyecto
COPY . /app/

# Expone el puerto que va a usar Gunicorn
EXPOSE 8000

# Comando por defecto para iniciar el servidor de producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

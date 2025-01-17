# Etapa de compilación
FROM python:3.11-slim as builder

# Instalamos las dependencias de compilación
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Creamos y activamos un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiamos solo los archivos necesarios para la instalación
COPY requirements.txt .

# Instalamos las dependencias en el entorno virtual
RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Etapa final
FROM python:3.11-slim

# Copiamos el entorno virtual de la etapa de compilación
COPY --from=builder /opt/venv /opt/venv

# Configuramos el entorno
ENV PATH="/opt/venv/bin:$PATH"
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copiamos solo los archivos necesarios de la aplicación
COPY ./challenge ./challenge

# Usuario no root por seguridad
RUN useradd -m appuser && chown -R appuser:appuser $APP_HOME
USER appuser

# Comando para ejecutar la aplicación
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
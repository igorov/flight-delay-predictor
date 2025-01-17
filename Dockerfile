# Etapa de compilación
FROM python:3.11-slim as builder

# Instalamos solo las dependencias mínimas necesarias para compilar
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Creamos y activamos un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Actualizamos pip y setuptools
RUN pip install --no-cache-dir -U pip setuptools wheel

# Instalamos las dependencias en orden específico para optimizar la caché
COPY requirements.txt .
RUN pip install --no-cache-dir \
    fastapi==0.115.6 \
    pydantic==2.10.5 \
    uvicorn==0.15.0 \
    python-decouple==3.8 \
    python-json-logger==3.2.1 \
    google-cloud-storage==2.19.0

# Instalamos las dependencias pesadas de ciencia de datos
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==1.3.5 \
    scikit-learn==1.3.2 \
    xgboost==2.1.3 \
    && find /opt/venv -type d -name "__pycache__" -exec rm -r {} + \
    && find /opt/venv -type f -name "*.pyc" -delete

# Etapa final
FROM python:3.11-slim-bullseye as final

# Copiamos solo el entorno virtual
COPY --from=builder /opt/venv /opt/venv

# Configuramos el entorno
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Copiamos solo los archivos de la aplicación
COPY ./challenge ./challenge

# Usuario no root por seguridad
RUN useradd -m appuser \
    && chown -R appuser:appuser $APP_HOME

USER appuser

EXPOSE 8080

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
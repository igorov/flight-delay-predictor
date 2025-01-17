export LOG_LEVEL=DEBUG
export THRESHOLD_IN_MINUTES=15
export GOOGLE_APPLICATION_CREDENTIALS=/home/igorov/reto/sa/pruebas1-448003-65a2da9ad46a.json

# Storage
export BUCKET_NAME=model-challenge
export MODEL_FILE=model_file/delay_model.json

python -m unittest tests/model/test_model.py
#python -m unittest tests/api/test_api.py
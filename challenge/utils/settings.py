from decouple import config

# Application config
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
THRESHOLD_IN_MINUTES = config("THRESHOLD_IN_MINUTES", default=5, cast=int)

# Storage
BUCKET_NAME = config("BUCKET_NAME")
MODEL_FILE = config("MODEL_FILE")
DATASET_FILE = config("DATASET_FILE")
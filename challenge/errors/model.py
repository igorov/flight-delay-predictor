class ModelError(Exception):
    """Excepción base para la clase ProcessData"""
    pass

class FitError(ModelError):
    """Excepción lanzada cuando los datos de entrada son inválidos"""
    pass

class PredictError(ModelError):
    """Excepción lanzada cuando faltan columnas requeridas en el DataFrame"""
    pass

class ProcessDataError(Exception):
    """Excepción base para la clase ProcessData"""
    pass


class InvalidDataError(ProcessDataError):
    """Excepción lanzada cuando los datos de entrada son inválidos"""
    pass


class MissingColumnError(ProcessDataError):
    """Excepción lanzada cuando faltan columnas requeridas en el DataFrame"""
    pass


class PreprocessingError(ProcessDataError):
    """Excepción lanzada durante el preprocesamiento de los datos"""
    pass

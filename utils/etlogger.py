import logging
import functools

logger = logging.getLogger(__name__)

ConsoleOutputHandler = logging.StreamHandler()
FileOutputHandler = logging.FileHandler('errorLogs.log')

ConsoleOutputHandler.setLevel(logging.WARNING)
FileOutputHandler.setLevel(logging.ERROR)

logger.addHandler(ConsoleOutputHandler)
logger.addHandler(FileOutputHandler)

logger = logging.getLogger('django')

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Capture the view name
        view_name = self.__class__.__name__ if hasattr(self, '__class__') else None
        # Capture the model name
        model_name = None
        if hasattr(self, 'queryset') and self.queryset is not None:
            model_name = self.queryset.model.__name__

        # Log additional context
        # logger.info(f"Function: {func.__name__}, View: {view_name}, Model: {model_name}, Args: {args}, Kwargs: {kwargs}")
        logger.info(f"Function: {func.__name__}, View: {view_name}, Model: {model_name}")

        # Call the original function
        return func(self, *args, **kwargs)
    return wrapper
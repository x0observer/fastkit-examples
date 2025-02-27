
from src.app.files.service import FileService
from src.app.files.router import FileRouter
# ...
file_router = FileRouter(service_cls=FileService, prefix="/files").get_router()
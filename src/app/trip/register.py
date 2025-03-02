
from src.app.trip.service import TripService
from src.app.trip.router import TripRouter


# file_service = get_file_service()  # ...
trip_router = TripRouter(service_cls=TripService, prefix="/trips").get_router()

from src.app.trip.service import TripService
from src.app.trip.router import TripRouter

# ...
trip_router = TripRouter(service_cls=TripService, prefix="/trips").get_router()
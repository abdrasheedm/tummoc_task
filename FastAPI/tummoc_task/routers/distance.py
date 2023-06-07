from fastapi import APIRouter
from .. import schemas, database
import math

router = APIRouter(
    tags=['Distance'],
)
get_db = database.get_db


# CALCULATE DISTANCE

@router.post("/distance")
def calculate_distance(request : schemas.Distance):
    # CALCULATING DISTANCE USING DISTANCE FORMULA
    distance = math.sqrt((request.lat2 - request.lat1)**2 + (request.lon2 - request.lon1)**2)
    return {"distance": distance}
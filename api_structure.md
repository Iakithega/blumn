# GET /api/plants/today
{
    "plants": [
        {
            "id": 1,
            "name": "Monstera",
            "last_watered": "2024-03-15",
            "last_fertilized": "2024-03-10",
            "days_since_watering": 2,
            "days_since_fertilizing": 7,
            "watering_schedule": 3,  # days
            "fertilizing_schedule": 14,  # days
            "needs_water": True,
            "needs_fertilizer": False
        },
        # ... more plants
    ]
}
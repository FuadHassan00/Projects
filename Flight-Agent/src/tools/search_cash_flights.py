import os
import serpapi
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from langchain_core.tools import tool
from src.core.exceptions import ValidationError
from src.core.validators import (validate_airports,validate_date_range,validate_passengers)


env_path = Path("resources/.env")

load_dotenv(env_path, override=True)

# Retrieve API key
api_key = os.getenv("SERP_API_KEY")

client = serpapi.Client(api_key=api_key.strip())

@tool
def search_cash_flights(
    origin: str,
    destination: str,
    flight_type: str,
    depart_date: str,
    return_date: str,
    num_of_adults: str,
    sort_by : str | None = None
):
    """
    Search for cash flight options using the Google Flights API via SerpApi.

    Use this tool to retrieve flight prices, airlines, schedules, durations,
    and available itineraries for a specified route and travel dates.

    Args:
        origin (str): Departure airport IATA code (e.g., "CLT").
        destination (str): Arrival airport IATA code (e.g., "LHR").
        flight_type (str): Flight type. "1" for round-trip or "2" for one-way.
        depart_date (str): Departure date in YYYY-MM-DD format.
        return_date (str): Return date in YYYY-MM-DD format.
            Required for round-trip flights.
        num_of_adults (str): Number of adult passengers (e.g., "1", "2").

    Returns:
        dict: Flight search results containing available itineraries,
        ticket prices, airline information, departure and arrival times,
        flight durations, and booking details.
    """

    try:
            validate_airports(origin, destination)
            validate_date_range(depart_date, return_date, flight_type)
            validate_passengers(num_of_adults)

            params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "currency": "USD",
            "type": flight_type,
            "outbound_date": depart_date,
            "return_date": return_date,
            "adults": num_of_adults,
            "sort_by": sort_by
        }
            # Execute SerpApi search
            results = client.search(params)
            return results
    except ValidationError as e:
            return {
                "status": "error",
                "error_type": "validation_error",
                "message": str(e)
            }

    except Exception as e:
            return {
                "status": "error",
                "error_type": "flight_search_error",
                "message": "Cash flight search failed"
            }


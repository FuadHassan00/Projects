import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from src.core.exceptions import ValidationError
from src.core.validators import validate_search_window
from langchain_core.tools import tool


env_path = Path("resources/.env")

load_dotenv(env_path, override=True)

# Retrieve API key
api_key = os.getenv("SEATS_AERO_API_KEY")

def payload() :
    url = "https://seats.aero/partnerapi/search"
    headers = {
        "accept": "application/json",
        "Partner-Authorization": api_key.strip()
    }
    return url, headers


def create_list_dict(search_response: dict) -> list[dict]:
    output = []

    for flight in search_response.get("data", []):
        output.append({
            "date": flight.get("Date"),
            "program": flight.get("Source"),

            "economy_points": (
                int(flight["YMileageCost"])
                if flight.get("YMileageCost") not in (None, "")
                else None
            ),
            "economy_taxes": (
                flight["YTotalTaxes"] / 100
                if flight.get("YTotalTaxes") is not None
                else None
            ),

            "premium_economy_points": (
                int(flight["WMileageCost"])
                if flight.get("WMileageCost") not in (None, "")
                else None
            ),
            "premium_economy_taxes": (
                flight["WTotalTaxes"] / 100
                if flight.get("WTotalTaxes") is not None
                else None
            ),

            "business_points": (
                int(flight["JMileageCost"])
                if flight.get("JMileageCost") not in (None, "")
                else None
            ),
            "business_taxes": (
                flight["JTotalTaxes"] / 100
                if flight.get("JTotalTaxes") is not None
                else None
            ),

            "first_class_points": (
                int(flight["FMileageCost"])
                if flight.get("FMileageCost") not in (None, "")
                else None
            ),
            "first_class_taxes": (
                flight["FTotalTaxes"] / 100
                if flight.get("FTotalTaxes") is not None
                else None
            ),

            "currency": flight.get("TaxesCurrency")
        })

    return output

@tool
def search_awards_flights(origin: list[str],destination: list[str],depart_date_start: str,depart_date_end: str):
    """
    Search for available award flights using airline miles or points
    through the seats.aero API.

    Retrieves award flight availability across one or more departure
    and destination airports within a specified date range.
    Results are ordered by lowest mileage cost.

    Args:
        origin (list[str]): List of departure airport IATA codes.
            Example: ["CLT", "JFK", "EWR"].

        destination (list[str]): List of destination airport IATA codes.
            Example: ["PRG", "WAW", "AMS"].

        depart_date_start (str): Earliest departure date to search,
            formatted as YYYY-MM-DD. Required.

        depart_date_end (str): Latest departure date to search,
            formatted as YYYY-MM-DD. Required. Must be on or
            after depart_date_start.

    Returns:
        list[dict] | dict:
            A list of dictionaries containing available award flight
            options, as produced by create_list_dict(), or a dictionary
            containing an error message if the request fails.

    Notes:
        - Searches award flights, not cash fares.
        - Supports multiple origin and destination airports.
        - Searches departures within the specified date range.
        - Requests up to 100 results per API call.
        - Results are requested in ascending mileage-cost order.
        - Availability depends on the seats.aero API response.
    """

    try:
            # Validate airport codes
            if not origin or not destination:
                raise ValidationError(
                    "Origin and destination airports are required"
                )
    
            for airport in origin + destination:
                if not isinstance(airport, str) or len(airport.strip()) != 3:
                    raise ValidationError(
                        "Airport codes must contain exactly 3 characters"
                    )
    
            # Validate departure date window
            validate_search_window(
                depart_date_start,
                depart_date_end
            )

            params = {
                "origin_airport": ",".join(origin),
                "destination_airport": ",".join(destination),
                "start_date": f"{depart_date_start}",
                "end_date": f"{depart_date_end}",
                "take": 100,
                "order_by": "lowest_mileage",
                "include_trips": True
                }
    
            url, headers = payload()
            
            
            response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=30
                )


            response.raise_for_status()
            data = response.json()
            
            flights = create_list_dict(data)
            
            return {
                        "status": "success",
                        "count": len(flights),
                        "flights": flights
                    }
            
    except ValidationError as e:
                    return {
                        "status": "error",
                        "error_type": "validation_error",
                        "message": str(e)
                    }
            
    except requests.exceptions.RequestException as e:
                    return {
                        "status": "error",
                        "error_type": "flight_search_error",
                        "message": f"Award flight API request failed: {e}"
                    }
            
    except ValueError as e:
                    return {
                        "status": "error",
                        "error_type": "response_error",
                        "message": f"Invalid API response: {e}"
                    }



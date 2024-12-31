import json
from Vehicles.Vehicle import Vehicle
from Vehicles.Suplement import *

class Json_Reader:

    @staticmethod
    def load_vehicles_from_file(file_path):
        """
        Reads a JSON file and parses it into a list of Vehicle objects.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Load the JSON data from the file

            vehicles = [
                Vehicle(
                    id=item["id"],
                    type=item["type"].lower(),
                    capacity=item["capacity_kg"],
                    autonomy=item["autonomy_km"],
                    speed=item["average_speed_kmh"]
                )
                for item in data
            ]

            return vehicles
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return []
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from file '{file_path}'")
            return []
        except KeyError as e:
            print(f"Error: Missing expected key in JSON data: {e}")
            return []
        
    
    def load_suplements_from_json(file_path):
        """
        Reads a JSON file and parses it into a list of Suplement objects.
        
        :param file_path: Path to the JSON file containing supplement data
        :return: List of Suplement objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Load JSON data from the file
    
            suplements = [
                Suplement(
                    urgency=item["urgency_level"],  # Location is used as the type here
                    location=item["location"],
                    quantity=item["required_quantity_kg"],
                    timeRemaining=item["remaining_time_seconds"]
                )
                for item in data
            ]
    
            return suplements
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return []
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from file '{file_path}'")
            return []
        except KeyError as e:
            print(f"Error: Missing expected key in JSON data: {e}")
            return []
    
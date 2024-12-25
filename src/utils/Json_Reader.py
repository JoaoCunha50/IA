import json
from Vehicles.Vehicle import Vehicle

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
                    type=item["type"],
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
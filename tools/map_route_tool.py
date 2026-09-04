# ============================================================
# MONSIGHT MAP & ROUTE TOOL
# ============================================================

class MapRouteTool:

    def __init__(self):
        # Simulated places and routes
        self.places = {
            "library": {
                "distance_m": 450,
                "walking_time_min": 6,
                "route": [
                    "Walk straight",
                    "Turn right",
                    "Continue for 200 meters",
                    "Turn left",
                    "Library is ahead"
                ]
            },

            "classroom": {
                "distance_m": 180,
                "walking_time_min": 3,
                "route": [
                    "Walk straight",
                    "Turn left",
                    "Continue for 80 meters",
                    "Classroom is ahead"
                ]
            },

            "canteen": {
                "distance_m": 300,
                "walking_time_min": 4,
                "route": [
                    "Walk straight",
                    "Turn right",
                    "Continue for 150 meters",
                    "Canteen is ahead"
                ]
            }
        }

    def find_destination(self, destination):
        """Find a destination."""

        destination = destination.lower().strip()

        if destination in self.places:
            return self.places[destination]

        return None

    def get_route(self, destination):
        """Return route information."""

        place = self.find_destination(destination)

        if place is None:
            return {
                "status": "not_found",
                "message": f"Destination '{destination}' not found."
            }

        return {
            "status": "success",
            "destination": destination,
            "distance_m": place["distance_m"],
            "walking_time_min": place["walking_time_min"],
            "route": place["route"]
        }

    def get_alternative_route(self, destination):
        """Provide a simple alternative route."""

        place = self.find_destination(destination)

        if place is None:
            return {
                "status": "not_found",
                "message": f"No alternative route available."
            }

        return {
            "status": "success",
            "destination": destination,
            "distance_m": place["distance_m"] + 80,
            "walking_time_min": place["walking_time_min"] + 2,
            "route": [
                "Walk straight",
                "Take the alternate path",
                "Continue ahead",
                f"Reach {destination}"
            ]
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("       MONSIGHT MAP & ROUTE TOOL")
    print("========================================")

    map_tool = MapRouteTool()

    destination = input("\nEnter destination: ")

    route = map_tool.get_route(destination)

    print("\nRoute Information")
    print("----------------------------------------")

    if route["status"] == "success":

        print("Destination:", route["destination"])
        print("Distance:", route["distance_m"], "meters")
        print("Walking Time:", route["walking_time_min"], "minutes")

        print("\nDirections:")

        for step_number, step in enumerate(
            route["route"],
            start=1
        ):
            print(f"{step_number}. {step}")

        print("\nAlternative Route")
        print("----------------------------------------")

        alternative = map_tool.get_alternative_route(destination)

        print("Distance:", alternative["distance_m"], "meters")
        print(
            "Walking Time:",
            alternative["walking_time_min"],
            "minutes"
        )

    else:
        print(route["message"])
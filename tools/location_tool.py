# ============================================================
# MONSIGHT LOCATION TOOL
# ============================================================

class LocationTool:

    def __init__(self):
        # Simulated starting location
        self.latitude = 12.9716
        self.longitude = 77.5946

        # Walking information
        self.direction = "NORTH"
        self.speed = 1.2          # meters per second
        self.distance_travelled = 0.0

    def get_location(self):
        """Return current location."""

        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def get_movement(self):
        """Return current movement information."""

        return {
            "direction": self.direction,
            "speed_mps": self.speed,
            "distance_travelled_m": self.distance_travelled
        }

    def update_movement(self, direction, speed, distance):
        """Update simulated movement."""

        self.direction = direction
        self.speed = speed
        self.distance_travelled += distance

    def get_status(self):
        """Return complete location status."""

        return {
            "location": self.get_location(),
            "movement": self.get_movement()
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    location = LocationTool()

    print("\n========================================")
    print("        MONSIGHT LOCATION TOOL")
    print("========================================")

    print("\nCurrent Location:")
    print(location.get_location())

    print("\nMovement:")
    print(location.get_movement())

    print("\nUpdating movement...")

    location.update_movement(
        direction="EAST",
        speed=1.4,
        distance=5
    )

    print("\nUpdated Status:")
    print(location.get_status())
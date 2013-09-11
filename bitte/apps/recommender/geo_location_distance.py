import math
import decimal

class Nearby:
    earth_radius = 6371.0  # for kms
    degrees_to_radians = math.pi / 180.0
    radians_to_degrees = 180.0 / math.pi

    def change_in_latitude(self, distance):
        "Given a distance north, return the change in latitude."
        return (distance / self.earth_radius) * self.radians_to_degrees

    def change_in_longitude(self, latitude, distance):
        "Given a latitude and a distance west, return the change in longitude."
        # Find the radius of a circle around the earth at given latitude.
        r = self.earth_radius * math.cos(latitude * self.degrees_to_radians)
        return (distance / r) * self.radians_to_degrees

    def bounding_box(self, latitude, longitude, distance):
        latitude = float(latitude)
        longitude = float(longitude)
        lat_change = self.change_in_latitude(distance)
        lat_max = latitude + lat_change
        lat_min = latitude - lat_change
        lon_change = self.change_in_longitude(latitude, distance)
        lon_max = longitude + lon_change
        lon_min = longitude - lon_change

        lat_max = decimal.Decimal(lat_max)
        lat_min = decimal.Decimal(lat_min)
        lon_max = decimal.Decimal(lon_max)
        lon_min = decimal.Decimal(lon_min)

        lat_max = round(lat_max,6)
        lat_min = round(lat_min,6)
        lon_max = round(lon_max,6)
        lon_min = round(lon_min,6)

        return (lon_max, lon_min, lat_max, lat_min)

    def test(self):
        lat = -12
        lon = -38

        lon_max, lon_min, lat_max, lat_min = self.bounding_box(lat, lon, 10)

        return (lon_max, lon_min, lat_max, lat_min)

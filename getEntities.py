import os
import json
import requests


#base_url = 'http://localhost:8082'
entities = ["/v1.0/Things", "/v1.0/Locations", "/v1.0/HistoricalLocations", "/v1.0/Sensors",
            "/v1.0/Datastreams", "/v1.0/ObservedProperties", "/v1.0/Observations", "/v1.0/FeaturesOfInterest"]


class getModel:
    def __init__(self, base_url):

        self.model = dict()
        for ent in entities:
            r = requests.get(base_url + ent)
            self.model[ent] = r.json()["value"]

    # Check if a entityname is already listed in a path
    # returns the entity if so and None if not
    def has_entity(self, path, name):
        for entity in self.model[path]:
            if name == entity["name"]:
                return entity
        return None


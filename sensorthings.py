import json

import requests
import getEntities


def build_unit_of_measurement(name, symbol, definition, **kwargs):
    unit = {'name': name, 'symbol': symbol, 'definition': definition}
    unit.update(kwargs)
    return unit


class SensorThingsClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.model = getEntities.getModel(base_url)

    def post_thing(self, name, description, properties=None, **kwargs):
        thing = {'name': name,
                 'description': description,
                 'properties': properties if properties else dict()}
        thing.update(kwargs)
        return self._post(path='/v1.0/Things', data=thing)

    def post_datastream(self, name, description, observation_type, unit_of_measurement, observed_property,
                        sensor, **kwargs):
        data_stream = {'name': name,
                       'description': description,
                       'observationType': observation_type,
                       'unitOfMeasurement': unit_of_measurement,
                       'ObservedProperty': observed_property,
                       'Sensor': sensor}
        data_stream.update(kwargs)
        return self._post(path='/v1.0/Datastreams', data=data_stream)

    def post_observed_property(self, name, description, definition, **kwargs):
        op = {'name': name, 'description': description, 'definition': definition}
        op.update(kwargs)
        return self._post(path='/v1.0/ObservedProperties', data=op)

    def post_sensor(self, name, description, encoding_type, metadata, **kwargs):
        sensor = {'name': name, 'description': description, 'encodingType': encoding_type,
                  'metadata': metadata}
        sensor.update(kwargs)
        return self._post(path='/v1.0/Sensors', data=sensor)

    # def _post(self, path, data, **kwargs):
    #     r = requests.post(self.base_url + path, data=json.dumps(data), **kwargs)
    #     r.raise_for_status()
    #     return r.json()

    def _post(self, path, data, **kwargs):
        entity = self.model.has_entity(path, data["name"])
        if entity is None:
            print("Added ", data["name"], " in path ", path)
            r = requests.post(self.base_url + path, data=json.dumps(data), **kwargs)
            r.raise_for_status()
            return r.json()
        else:
            print("already have ", data["name"])
            return entity

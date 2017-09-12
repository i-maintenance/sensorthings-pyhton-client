import click
from sensorthings import build_unit_of_measurement, SensorThingsClient


@click.command()
@click.option('--server', default='http://localhost:8080', help='URL of SensorThings server')
@click.option('--printer_id', help='Id of printer to add ')
def create_cm_temperatures(server, printer_id):
    """Creates model of Ultimaker's temperature sensors on SensorThings API server"""

    print("Creating SensorThings model of Ultimaker's temperature sensors on {}".format(server))

    # create client for SensorThings API
    # noinspection PyUnusedLocal
    st_client = SensorThingsClient(server)

    # ********************************************************************************************************
    # Create datastream for sensing temperatures measurements for each sensor
    # ********************************************************************************************************

    # Mapping for Sensors as shown here:
    # https://secure.salzburgresearch.at/wiki/display/IM/CM+der+Temperatur+am+3D-Drucker+-+Messfeld
    sensors = [["S321", "wall left-back-top"], ["S211", "wall left-front-top"],
               ["S111", "wall right-back-top"],
               ["S412", "wall right-front-top"], ["S212", "wall left-back-bottom"],
               ["S311", "wall left-front-bottom"],
               ["S411", "wall right-back-bottom"], ["S121", "wall right-front-top"],
               ["S312", "wall left-middle-middle"],
               ["S122", "wall right-middle-middle"],
               ["S512", "print bed-back-left"], ["S511", "print-bed back-middle"],
               ["S621", "print-bed back-right"],
               ["S421", "print-bed middle-left"], ["S622", "print-bed middle-right"],
               ["S422", "print-bed front-left"],
               ["S612", "print-bed front-middle"], ["S611", "print-bed front-right"],
               ["S322", "stepper-motor-y-axis"], ["S112", "stepper-motor-x-axis"]]

    # add the prefix "Temp" to the sensor number e.g.: ["S312", "Temp312", "wall left-back-top"]
    sensors = [[i[0], i[0].replace("S", "Temp"), i[1]] for i in sensors]

    temperature_sensor_ids = dict()
    sensor_op_ids = dict()
    sensor_ds_ids = dict()

    for sensor_id, sensor_code, sensor_desc in sensors:
        # set temperature observations
        temperature_sensor_ids[sensor_id] = st_client.post_sensor(name=sensor_code,
                                                                  description=sensor_desc,
                                                                  encoding_type='application/pdf',
                                                                  metadata='https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf').get('@iot.id')

        sensor_op_ids[sensor_id] = st_client.post_observed_property(name='Temperature',
                                                                    description=sensor_desc,
                                                                    definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#ThermodynamicTemperature').get('@iot.id')

        sensor_ds_ids[sensor_id] = st_client.post_datastream(name=sensor_code,
                                                             description=sensor_desc,
                                                             observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
                                                             unit_of_measurement=temperature_unit,
                                                             observed_property={'@iot.id': sensor_op_ids[sensor_id]},
                                                             sensor={'@iot.id': temperature_sensor_ids[sensor_id]},
                                                             Thing={'@iot.id': printer_id}).get('@iot.id')


# ************************************************************************************************************
# Create definition of units
# ************************************************************************************************************
temperature_unit = build_unit_of_measurement(name='Degree Celsius',
                                             symbol='degC',
                                             definition='http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius')

if __name__ == '__main__':
    create_cm_temperatures()

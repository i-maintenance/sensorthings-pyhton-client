import click
from sensorthings import build_unit_of_measurement, SensorThingsClient


@click.command()
@click.option('--server', default='http://localhost:8080', help='URL of SensorThings server')
def create_ultimaker(server):
    """Creates model of Ultimaker on SensorThings API server"""

    print('Creating SensorThings model of Ultimaker on {}'.format(server))

    # create client for SensorThings API
    st_client = SensorThingsClient(server)

    # ********************************************************************************************************
    # Create printer (thing)
    # ********************************************************************************************************

    # create 3D printer in lab
    printer_id = st_client.post_thing(
        name='Ultimaker 2',
        description='3D printer Ultimaker 2 in IoT Lab',
        properties={
            'specification': 'https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf'}
    ).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for filament consumption measurements (fila.distance)
    # ********************************************************************************************************
    distance_sensor_id = st_client.post_sensor(
        name='<<TODO: rotation sensor name>>',
        description='<<TODO: rotation sensor name>>',
        encoding_type='application/pdf',
        medadata='<<TODO>>').get('@iot.id')

    fila_distance_op_id = st_client.post_observed_property(
        name='Filament Length',
        description='Distance of fed filament',
        definition='<<TODO >>').get('@iot.id')

    fila_distance_ds_id = st_client.post_datastream(
        name='Filament Usage DS',
        description='Distance of used filament',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=milimeter_unit,
        observed_property={"@iot.id": fila_distance_op_id},
        sensor={"@iot.id": distance_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for skid detection measurements (fila.skidrate & fila.skidcount)
    # ********************************************************************************************************

    skid_sensor_id = st_client.post_sensor(
        name='<<TODO: skid sensor name>>',
        description='<<TODO: rotation sensor name>>',
        encoding_type='application/pdf',
        medadata='<<TODO>>').get('@iot.id')

    # Skid rate observations
    skid_rate_op_id = st_client.post_observed_property(
        name='Skidrate of Filament',
        description='Rate of skids, which occurred during print',
        definition='<<TODO >>').get('@iot.id')
    skid_rate_ds_id = st_client.post_datastream(
        name='Filament Skidrate DS',
        description='Skid rate at feeding time.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=per_meter_unit,
        observed_property={"@iot.id": skid_rate_op_id},
        sensor={"@iot.id": skid_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Skid count observations
    skid_count_op_id = st_client.post_observed_property(
        name='Skid Count',
        description='Absolute number of skids, which occurred during print',
        definition='<<TODO >>').get('@iot.id')
    skid_count_ds_id = st_client.post_datastream(
        name='Skid Count DS',
        description='Absolute number of skids, which occurred during print',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=counting_unit,
        observed_property={"@iot.id": skid_count_op_id},
        sensor={"@iot.id": skid_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for sensing temperatures measurements (temp, temp.bed.current & temp.nozzle.current)
    # ********************************************************************************************************

    temperature_sensor_id = st_client.post_sensor(
        name='<<TODO: name of sensor>>',
        description='<<TODO>>',
        encoding_type='application/pdf',
        medadata='<<TODO>>').get('@iot.id')

    # Ambient temperature observations
    amb_temp_op_id = st_client.post_observed_property(
        name='Ambient Temperature',
        description='Temperature of surrounding during print.',
        definition='<<TODO >>').get('@iot.id')
    amb_temp_ds_id = st_client.post_datastream(
        name='Ambient Temperature DS',
        description='Observations of temperature of surrounding during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": amb_temp_op_id},
        sensor={"@iot.id": temperature_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Bed temperature observations
    bed_temp_op_id = st_client.post_observed_property(
        name='Bed Temperature',
        description='Temperature of base plate during print.',
        definition='<<TODO >>').get('@iot.id')
    bed_temp_ds_id = st_client.post_datastream(
        name='Bed Temperature DS',
        description='Observations of temperature of base plate during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": bed_temp_op_id},
        sensor={"@iot.id": temperature_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Nozzle temperature observations
    nozzle_temp_op_id = st_client.post_observed_property(
        name='Nozzle Temperature',
        description='Temperature of nozzle during print.',
        definition='<<TODO >>').get('@iot.id')
    nozzle_temp_ds_id = st_client.post_datastream(
        name='Nozzle Temperature DS',
        description='Observations of temperature of nozzle during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": nozzle_temp_op_id},
        sensor={"@iot.id": temperature_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for airquality measurements (airquality)
    # ********************************************************************************************************

    airquality_sensor_id = st_client.post_sensor(
        name='VELUX Raumluftfühler',
        description='Messung der Raumluftqualität auf Basis flüchtiger organischer Verbindungen (VOCs).',
        encoding_type='text/html',
        medadata='http://www.velux.de/produkte/lueftungsloesungen-belueftung/raumluftfuehler').get('@iot.id')

    airquality_op_id = st_client.post_observed_property(
        name='Airquality',
        description='Quality of air during print.',
        definition='<<TODO >>').get('@iot.id')
    airquality_ds_id = st_client.post_datastream(
        name='Airquality DS',
        description='Observations of airquality during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=airquality_unit,
        observed_property={"@iot.id": airquality_op_id},
        sensor={"@iot.id": airquality_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for z-position of printer head (head.pos.z)
    # ********************************************************************************************************

    printer_head_pos_sensor_id = st_client.post_sensor(
        name='<<TODO>>',
        description='<<TODO>>',
        encoding_type='application/pdf',
        medadata='<<TODO>>').get('@iot.id')

    printer_head_pos_op_id = st_client.post_observed_property(
        name='Printer Head Z-Coordinate',
        description='Z-Coordinates of printer head.',
        definition='<<TODO >>').get('@iot.id')
    printer_head_pos_ds_id = st_client.post_datastream(
        name='Printer Head Z-Coordinate DS',
        description='Observations of z-coordinate of printer head.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=milimeter_unit,
        observed_property={"@iot.id": printer_head_pos_op_id},
        sensor={"@iot.id": printer_head_pos_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for extrusion of filament (extrusion)
    # ********************************************************************************************************

    extrusion_sensor_id = st_client.post_sensor(
        name='<<TODO>>',
        description='<<TODO>>',
        encoding_type='application/pdf',
        medadata='<<TODO>>').get('@iot.id')

    extrusion_op_id = st_client.post_observed_property(
        name='Filament Usage',
        description='Volume of use filament',
        definition='<<TODO >>').get('@iot.id')
    extrusion_ds_id = st_client.post_datastream(
        name='Filament Usage DS',
        description='Observations used filament during print',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=cubic_milimeter_unit,
        observed_property={"@iot.id": extrusion_op_id},
        sensor={"@iot.id": extrusion_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    print('Created printer with id {}'.format(printer_id))


# ************************************************************************************************************
# Create definition of units
# ************************************************************************************************************
milimeter_unit = build_unit_of_measurement(
    name='Milimeter',
    symbol='mm',
    definition='http://qudt.org/vocab/unit/MilliM')
per_meter_unit = build_unit_of_measurement(
    name='Units per meter',
    symbol='1/m',
    definition='<<TODO>>')
counting_unit = build_unit_of_measurement(
    name='Counting Unit',
    symbol='1',
    definition='<<TODO>>')
temperature_unit = build_unit_of_measurement(
    name='Degree Celsius',
    symbol='degC',
    definition='http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius')
airquality_unit = build_unit_of_measurement(
    name='Volatile Organic Compounds',
    symbol='VOC',
    definition='https://en.wikipedia.org/wiki/Volatile_organic_compound')
cubic_milimeter_unit = build_unit_of_measurement(
    name='Cubic Milimeter',
    symbol='mm3',
    definition='http://qudt.org/vocab/unit#CubicMiliaMeter')

if __name__ == '__main__':
    create_ultimaker()

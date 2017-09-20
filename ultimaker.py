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
            'specification': 'https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf',
            'isprong_uuid': '77371300-a534-4416-a640-39c559c34e13'}
    ).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for filament consumption measurements (fila.distance)
    # ********************************************************************************************************
    filament_sensor_id = st_client.post_sensor(
        name='Filament Sensor',
        description='The Filament Sensor measures the filament feeding process of the Ultimaker 2 3D printer by using the X4-encoding',
        encoding_type='application/pdf',
        encoding_description='http://www.motioncontroltips.com/faq-what-do-x1-x2-and-x4-position-encoding-mean-for-incremental-encoders/',
        metadata='https://www.thingiverse.com/thing:1733104').get('@iot.id')

    fila_distance_op_id = st_client.post_observed_property(
        name='Filament Length',
        description='Distance of fed filament',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#Length').get('@iot.id')

    fila_distance_ds_id = st_client.post_datastream(
        name='Filament Usage DS',
        description='Distance of used filament',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=milimeter_unit,
        observed_property={"@iot.id": fila_distance_op_id},
        sensor={"@iot.id": filament_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for skid detection measurements (fila.skidrate & fila.skidcount)
    # ********************************************************************************************************

    # Skid rate observations
    skid_rate_op_id = st_client.post_observed_property(
        name='Skidrate of Filament',
        description='Rate of skids per unit length, smoothed over 0.1 meter',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#InverseLength').get('@iot.id')
    skid_rate_ds_id = st_client.post_datastream(
        name='Filament Skidrate DS',
        description='Skid rate per unit length at feeding time.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=per_meter_unit,
        observed_property={"@iot.id": skid_rate_op_id},
        sensor={"@iot.id": filament_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Skid count observations
    skid_count_op_id = st_client.post_observed_property(
        name='Skid Count',
        description='Cumulated number of skids, which occurred during a specific print',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#Dimensionless').get('@iot.id')
    skid_count_ds_id = st_client.post_datastream(
        name='Skid Count DS',
        description='Cumulated number of skids, which occurred during a specific print',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=counting_unit,
        observed_property={"@iot.id": skid_count_op_id},
        sensor={"@iot.id": filament_sensor_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for sensing temperatures measurements (temp, temp.bed.current & temp.nozzle.current)
    # ********************************************************************************************************

    temperature_sensor_air_id = st_client.post_sensor(
        name='Air temperature sensor',
        description='NTC temperature sensor for air',
        encoding_type='application/pdf',
        metadata='https://shop.bb-sensors.com/out/media/Datasheet_NTC%20Sensor_0365%200020-12.pdf').get('@iot.id')

    # Ambient temperature observations
    amb_temp_op_id = st_client.post_observed_property(
        name='Ambient Temperature',
        description='Temperature of surrounding during print.',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#ThermodynamicTemperature').get(
        '@iot.id')
    amb_temp_ds_id = st_client.post_datastream(
        name='Ambient Temperature DS',
        description='Observations of temperature of surrounding during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": amb_temp_op_id},
        sensor={"@iot.id": temperature_sensor_air_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Bed temperature observations
    temperature_sensor_bed_id = st_client.post_sensor(
        name='Ultimaker 2 internal Temperature Sensor',
        description='The Ultimaker 2 is featured with internal PT100 sensors',
        encoding_type='application/pdf',
        metadata='https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf').get(
        '@iot.id')

    bed_temp_op_id = st_client.post_observed_property(
        name='Bed Temperature',
        description='Temperature of base plate during print.',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#ThermodynamicTemperature').get(
        '@iot.id')
    bed_temp_ds_id = st_client.post_datastream(
        name='Bed Temperature DS',
        description='Observations of temperature of base plate during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": bed_temp_op_id},
        sensor={"@iot.id": temperature_sensor_bed_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # Nozzle temperature observations
    temperature_sensor_nozzle_id = st_client.post_sensor(
        name='Ultimaker 2 internal Nozzle Temperature Sensor',
        description='The Ultimaker 2 is featured with internal PT100 sensor',
        encoding_type='application/pdf',
        metadata='https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf').get(
        '@iot.id')

    nozzle_temp_op_id = st_client.post_observed_property(
        name='Nozzle Temperature',
        description='Temperature of nozzle during print.',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#ThermodynamicTemperature').get(
        '@iot.id')
    nozzle_temp_ds_id = st_client.post_datastream(
        name='Nozzle Temperature DS',
        description='Observations of temperature of nozzle during print.',
        observation_type='http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
        unit_of_measurement=temperature_unit,
        observed_property={"@iot.id": nozzle_temp_op_id},
        sensor={"@iot.id": temperature_sensor_nozzle_id},
        Thing={"@iot.id": printer_id}).get('@iot.id')

    # ********************************************************************************************************
    # Create datastream for airquality measurements (airquality)
    # ********************************************************************************************************

    airquality_sensor_id = st_client.post_sensor(
        name='VELUX Raumluftfuehler',
        description='Messung der Raumluftqualitaet auf Basis fluechtiger organischer Verbindungen (VOCs).',
        encoding_type='application/pdf',
        metadata='http://www.velux.de/produkte/lueftungsloesungen-belueftung/raumluftfuehler').get('@iot.id')

    airquality_op_id = st_client.post_observed_property(
        name='Airquality',
        description='Quality of air during print.',
        definition='https://en.wikipedia.org/wiki/Volatile_organic_compound').get('@iot.id')
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
        name='Print Head position Z',
        description='Print Head position Z-axis (height)',
        encoding_type='application/pdf',
        metadata='https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf').get(
        '@iot.id')

    printer_head_pos_op_id = st_client.post_observed_property(
        name='Printer Head Z-Coordinate',
        description='Z-Coordinate of printer head.',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#Length').get('@iot.id')
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
        name='Planned Filament Extrusion',
        description='Volume of Filament feeded by the printer',
        encoding_type='application/pdf',
        metadata='https://ultimaker.com/file/download/productgroup/Ultimaker%202+%20specification%20sheet.pdf/5819be416ae76.pdf').get(
        '@iot.id')

    extrusion_op_id = st_client.post_observed_property(
        name='Filament Usage',
        description='Volume of used filament',
        definition='http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#Volume').get('@iot.id')
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
    definition='http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#MilliM')
per_meter_unit = build_unit_of_measurement(
    name='Units per meter',
    symbol='1/m',
    definition='http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#PerMeter')
counting_unit = build_unit_of_measurement(
    name='Counting Unit',
    symbol='1',
    definition='http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Number')
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
    definition='http://qudt.org/vocab/unit/MilliM3')

if __name__ == '__main__':
    create_ultimaker()

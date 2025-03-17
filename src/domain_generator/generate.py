import json
from pathlib import Path
from typing import List

import httpx
import lxml
import pika
from pydantic.error_wrappers import ValidationError

from domain_generator import get_shortest_path
from domain_generator.schemas import GaugeData, ProcessedData, Site
from domain_generator.settings import Settings
from domain_generator.utils import get

settings = Settings()

def pull_nwm_inputs(forecast, settings: Settings) -> ProcessedData:
    forecast_endpoint = f"{settings.BASE_URL}/gauges/{forecast.lid}/stageflow/forecast"
    site_data = get(forecast_endpoint).json()
    if site_data["data"][0]["secondary"] == -999:
        return None
    else:
        metadata_endpoint = f"{settings.BASE_URL}/reaches/{forecast.reachId}"
        downstream_metadata = get(metadata_endpoint).json()
        downstream_reach_id = int(downstream_metadata["route"]["downstream"][0]["reachId"])
        processed_data = ProcessedData(
            lid = forecast.lid,
            start_id = downstream_reach_id,
            end_id = downstream_reach_id,
        )
    return processed_data

def format_xml(product_text: str, settings: Settings) -> List[GaugeData]:
    """A function to format the product text from HML into valid XML segments
    """
    xml_split = product_text.split("?xml")
    forecasts = []

    # ignore the first one since it's not valid XML
    for i in range(1, len(xml_split)):
        xml_segment = "<?xml" + xml_split[i][:-2]  # adding removed XML tag, and removed trailing tags
        try:
            site = Site.from_xml(xml_segment)
        except lxml.etree.XMLSyntaxError:
            xml_segment = xml_segment.split("</site>")[0] + "</site>"  # Removing extra content at end of document
            site = Site.from_xml(xml_segment)
        endpoint = f"{settings.BASE_URL}/gauges/{site.properties['id']}"
        try:
            forecast = get(endpoint).json()
            try:
                gauge_data = GaugeData(**forecast)
            except ValidationError:
                # There was no forecast/record for the site given
                continue
            forecasts.append(gauge_data)
        except httpx.HTTPStatusError:
            # There was no forecast/record for the site given
            # print(f"{endpoint} hit 404 error: {str(e)}")
            continue
            
    return forecasts 

def run(
   ch: pika.channel.Channel,
   method: pika.spec.Basic.Deliver, 
   properties: pika.spec.BasicProperties,
   body: bytes
):
    hml = json.loads(body.decode())
    print(f"Reading forecast for {hml['rdf']}, issued at {hml['issuance_time']}")
    site_data = get(hml["rdf"], headers=settings.headers).json()
    gpkg_path = Path.cwd() / settings.gpkg_path
    forecasts = format_xml(site_data["productText"], settings)
    if len(forecasts) == 0:
        # There is no forecast present in this message. End the process
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        for forecast in forecasts:
            processed_data = pull_nwm_inputs(forecast, settings)
            if processed_data is None:
                # The streamflow forecast is -999
                ch.basic_ack(delivery_tag=method.delivery_tag)
            filepath = Path.cwd / f"{processed_data.lid}.gpkg"
            if filepath.exists():
                # The gpkg already exists
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                # Generating the domain
                get_shortest_path(
                    start_id=processed_data.start_id,
                    end_id=processed_data.start_id,
                    gpkg=gpkg_path,
                    filename=processed_data.lid,
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

def generate_domains() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(settings.pika_url))
    channel = connection.channel()

    channel.queue_declare(queue=settings.flooded_data_queue, durable=True)
    print(f' [*] Waiting for messages from Queue on URL: {settings.pika_url}')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.flooded_data_queue, on_message_callback=run)

    channel.start_consuming()

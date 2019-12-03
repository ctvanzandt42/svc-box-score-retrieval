import json
from datetime import date, timedelta
from configparser import ConfigParser
import pika
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

CONFIG = ConfigParser()
CONFIG.read('nba_app.properties')

RABBIT_HOST = CONFIG['nba']['RABBIT_HOST']
EXCHANGE = CONFIG['nba']['EXCHANGE']
ROUTING_KEY = CONFIG['nba']['ROUTING_KEY']

YESTERDAY = date.today() - timedelta(days=1)
BOX_SCORE_JSON = client.player_box_scores(day=YESTERDAY.day,
                            month=YESTERDAY.month,
                            year=YESTERDAY.year,
                            output_type=OutputType.JSON)

MESSAGE = json.dumps(BOX_SCORE_JSON).encode('utf-8')

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
CHANNEL = CONNECTION.channel()

CHANNEL.basic_publish(exchange=EXCHANGE,
                      routing_key=ROUTING_KEY,
                      body=MESSAGE)

CONNECTION.close()

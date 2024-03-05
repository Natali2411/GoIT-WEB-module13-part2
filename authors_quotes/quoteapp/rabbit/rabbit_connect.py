import time
from typing import Tuple

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from authors_quotes.settings import (RABBITMQ_EXCHANGE, RABBITMQ_QUEUE,
                                     RABBITMQ_PASSWORD, RABBITMQ_HOST,
                                     RABBITMQ_PORT, RABBITMQ_USER)
from pika.exceptions import AMQPConnectionError


def handle_connection_error(err_type: Exception):
    def wrapper_1(func):
        def wrapper_2(*args, **kwargs):
            retries = 10
            while retries > 0:
                retries -= 1
                try:
                    return func()
                except err_type as err:
                    time.sleep(1)
                    print(err)
        return wrapper_2
    return wrapper_1


@handle_connection_error(AMQPConnectionError)
def make_channel() -> Tuple[BlockingChannel, BlockingConnection]:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials
        )
    )
    channel = connection.channel()
    return channel, connection


def make_exchange_queue_bind(exchange_name: str = RABBITMQ_EXCHANGE,
                             queue_name: str = RABBITMQ_QUEUE):
    channel, connection = make_channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    return channel, connection

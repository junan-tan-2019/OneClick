import pika
import mysql.connector
import json
import time
import ssl
from os import environ
from urllib.parse import urlparse


db_url = urlparse(environ.get('db_conn'))

hostname = environ.get('rabbitmq_host')
port = environ.get('rabbitmq_port')

# parameters = pika.ConnectionParameters(host=hostname,
#                                        port=port
#                                        )
if environ.get('stage') == 'production':
    ssl_enabled = True
else:
    ssl_enabled = False

if ssl_enabled:
    username = environ.get('rabbitmq_username')
    password = environ.get('rabbitmq_password')
    credentials = pika.PlainCredentials(username, password)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    parameters = pika.ConnectionParameters(host=hostname,
                                           port=port,
                                           virtual_host='/',
                                           credentials=credentials,
                                           ssl_options=pika.SSLOptions(context)
                                           )
else:
    parameters = pika.ConnectionParameters(host=hostname,
                                           port=port)


connected = False

start_time = time.time()

print('Connecting to broker...')

while not connected:
    try:
        connection = pika.BlockingConnection(parameters)
        connected = True
    except pika.exceptions.AMQPConnectionError:
        if time.time() - start_time > 20:
            exit(1)

print('CONNECTED TO BROKER!')

channel = connection.channel()
exchange_name = "notifications"
exchange_type = "topic"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type=exchange_type, durable=True)

queue_name = 'collection_num'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name, routing_key='unique_ref')


def callback(channel, method, properties, body):
    message_body = json.loads(body)
    unique_ref = message_body['unique_ref']
    location = message_body['location']
    phone_number = message_body['phone_number']

    try:
        cnx = mysql.connector.connect(
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            database='collection')

        cursor = cnx.cursor()
        cursor.execute('''INSERT INTO `item_collection` (`unique_ref`, `location`, `phone_number`)
         VALUES (%s, %s, %s);''', (unique_ref, location, phone_number))

        print("Successfully insert the new collector into database!")
        cnx.commit()
        cnx.close()
        print(f"Success, inserted {unique_ref}, {location}")
    except mysql.connector.Error as error:
        print(f"FAIL, Unable to insert. Due to {error}")


channel.basic_consume(queue=queue_name, on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()

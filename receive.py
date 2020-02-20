import time
import pika
import sys
import pika.exceptions as exc


def callback(ch, method, properties, body):
    try:
        print(f"[x] Received {body}")
        print(properties)
        time.sleep(2)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[x] Done {body}")
    except exc.AMQPConnectionError as e:
        print(e)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=True)

queue_name = ''.join(sys.argv[1:])
print(queue_name)
result = channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange='logs', queue=queue_name)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


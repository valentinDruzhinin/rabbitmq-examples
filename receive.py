import time
import pika
import pika.exceptions as exc

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def callback(ch, method, properties, body):
    try:
        print(f"[x] Received {body}")
        time.sleep(2)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[x] Done {body}")
    except exc.AMQPConnectionError as e:
        print(e)


queue_name = 'hello'
channel.queue_declare(queue=queue_name, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


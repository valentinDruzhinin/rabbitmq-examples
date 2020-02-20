import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

try:
    queue_name = 'hello'
    channel.queue_declare(queue=queue_name, durable=True)
    for m in list(range(1, 21)):
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=str(m),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        print(f'Sent {m}')
except Exception as e:
    print(e)
finally:
    connection.close()

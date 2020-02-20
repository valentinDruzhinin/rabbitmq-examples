import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

try:
    channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=True)
    for m in list(range(1, 21)):
        channel.basic_publish(
            exchange='logs',
            routing_key='',
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

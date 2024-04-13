import pika
from model import Contact
import connect
import sys


def main():
    # Створення об'єкта credentials для автентифікації у RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')

    # Створення з'єднання з RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

    # Створення каналу зв'язку з RabbitMQ
    channel = connection.channel()

    # Оголошення черги 'sms_send_list'
    channel.queue_declare(queue='sms_send_list')

    # Визначення функції зворотнього виклику для обробки отриманих повідомлень
    def callback(ch, method, properties, body):
        print(f'[x] SMS received {body.decode()}')  # Вивід отриманого повідомлення

    # Підписка на чергу 'sms_send_list' з викликом функції зворотнього виклику callback
    channel.basic_consume(queue='sms_send_list', on_message_callback=callback, auto_ack=True)

    # Вивід повідомлення про очікування повідомлень
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Початок споживання (чекання) повідомлень з черги
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()  # Виклик головної функції main()
    except KeyboardInterrupt:
        print('Interrupted')  # Вивід повідомлення про переривання
        sys.exit(0)  # Вихід з програми при перериванні

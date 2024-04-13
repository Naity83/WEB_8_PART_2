import pika  
from model import Contact  
import connect  

def main():
    # Креденціали для з'єднання з RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    
    # Створення з'єднання з RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()  # Створення каналу зв'язку з RabbitMQ

    # Оголошення черг RabbitMQ для електронної пошти і sms
    channel.queue_declare(queue='email_send_list')
    channel.queue_declare(queue='sms_send_list')

    # Отримання списку контактів з бази даних
    contacts = Contact.objects()

    # Ітерація по кожному контакту
    for contact in contacts:
        # Відправка повідомлення в чергу email_send_list або sms_send_list залежно від пріоритету
        if contact.email_priority:
            channel.basic_publish(exchange='',
                                  routing_key='email_send_list',
                                  body=f'Hello, {contact.full_name}!'.encode())
        else:
            channel.basic_publish(exchange='',
                                  routing_key='sms_send_list',
                                  body=f'Hello, {contact.full_name}!'.encode())
        
        # Оновлення статусу send_message в базі даних
        contact.update(send_message=True)

    # Закриття з'єднання з RabbitMQ
    connection.close()

# Перевірка, чи файл запущено напряму, а не імпортовано
if __name__ == '__main__':
    main()


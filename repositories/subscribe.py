import redis


r = redis.StrictRedis(
    host='localhost',
    port=6379,
    decode_responses=True
)


def handle_message(message):
    print(f"Получено сообщение: {message['data']}")


if __name__ == "__main__":
    pubsub = r.pubsub()
    pubsub.subscribe('created_order')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_message(message)
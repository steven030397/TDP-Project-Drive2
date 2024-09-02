import random
import time
from tembo_pgmq_python import Message, PGMQueue


if __name__ == '__main__':
    host = "localhost"
    port = 5432
    username = "postgres"
    password = "postgres"
    database = "postgres"

    num_messages = 10000
    partition_interval = 10000
    retention_interval = None

    rnd = random.randint(0, 100)
    test_queue = "bench_queue_sample"

    queue = PGMQueue(host=host, port=port, username=username, password=password, database=database)
    no_message_timeout = 0

    while no_message_timeout < 5:
        try:
            message: Message = queue.pop(test_queue)  # type: ignore
            print("Consumed message: {}".format(message.message["payload"]))
            no_message_timeout = 0

        except IndexError:
            no_message_timeout += 1
            print("No more messages for {no_message_timeout} consecutive reads")
            time.sleep(0.500)
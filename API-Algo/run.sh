#!/bin/bash

python3 producer.py > /tmp/producer.out &
sleep 2

for i in $(seq 1 5)
do
  python3 consumer.py > /tmp/consumer_${i}.out &
done

wait

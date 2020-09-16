# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:24:31 2020

@author: mspiteri
"""

import pika, sys, os, json

max_value = - 2**63


def main():
    global max_value
    
    max_window_size = 100
    window = [max_value] * max_window_size

    def get_max_mich(new_val, out_val):

        global max_value

        if (new_val >= max_value):
            max_value = new_val

        elif (out_val == max_value):
            max_value = max(window)

    def compute_max(ch, method, properties, body):
        global max_value
        body_decoded = json.loads(body)

        window.append(body_decoded['rand'])

        outgoing_value = window.pop(0)
        new_value = body_decoded['rand']

        #calculate max
        get_max_mich(new_value, outgoing_value)

        # Encode in JSON
        msg = {"rand": body_decoded['rand'], "sequence_number": body_decoded['sequence_number'], "running_max" : max_value}
        message = json.dumps(msg)
        # print(message)

        #Publish to topic
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        op_channel = connection.channel()
        op_channel.queue_declare(queue="solution")
        op_channel.basic_publish(exchange="", routing_key= "solution", body=message)
        # print(op_channel)


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rand')
       
    channel.basic_consume(queue='rand', on_message_callback=compute_max, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:24:31 2020

@author: mspiteri
"""

import pika, sys, os, json

#setting a global variable called max_value, the initial value is set to the smallest value possible
max_value = - 2**63 

def main():

    #declaring that changes to the variable max_value shall overwrite the global value
    global max_value
    
    #initialize the window size over which the running max shall be computed
    max_window_size = 100 

    #initialize a queue "window" of size max_window_size and which contains the smallest integer values possible
    window = [max_value] * max_window_size 

    #function to calculate maximum
    def get_max(new_val, out_val):

        #changes to max_value shall overwrite the global value
        global max_value

        #update the max_value if the new incoming integer is higher than the max_value
        if (new_val >= max_value):
            max_value = new_val

        #if the max value has been popped, using Python in-built function to calculate max
        elif (out_val == max_value):
            max_value = max(window)

    #this function will read from the 'rand' queue, decode it from JSON, compute the max value, encode it in JSON and publish it to the 'solution' queue
    def compute_max(ch, method, properties, body):
        
        #changes to max_value shall overwrite the global value
        global max_value

        #decode the JSON formatted input value from the 'rand' queue
        body_decoded = json.loads(body)

        #append the window with the new value from the 'rand' queue
        window.append(body_decoded['rand'])

        #pop value from front of window queue and assign to variable "outgoing_value"
        outgoing_value = window.pop(0)

        #assign neew value from 'rand' queue to variable "new_value"
        new_value = body_decoded['rand']

        #Calculate max by calling "get_max" function and passing
        get_max(new_value, outgoing_value)

        #Encode "rand", "sequence_number" and "running_max" in JSON
        msg = {"rand": body_decoded['rand'], "sequence_number": body_decoded['sequence_number'], "running_max" : max_value}
        message = json.dumps(msg)

        #Initialize connection to localhost using pika
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        #Declare channel named "op_channel"
        op_channel = connection.channel()

        #Declare queue "solution" on channel "op_channel"
        op_channel.queue_declare(queue="solution")

        #Publish to topic queue 'solution'
        op_channel.basic_publish(exchange="", routing_key= "solution", body=message)
    

    #Initialize connection to localhost using pika
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    #Declare channel named "channel"
    channel = connection.channel()

    #Declare queue "rand" on channel "channel"
    channel.queue_declare(queue='rand')
       
    #Consume messages from the queue "rand" on channel "channel". Upon receipt of each message call function "compute_max"
    channel.basic_consume(queue='rand', on_message_callback=compute_max, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    #Consume random number essages
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

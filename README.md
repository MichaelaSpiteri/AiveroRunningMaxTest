# Challenge the coder

## Programming exercise for software, robotics and machine vision engineer candidates at Aivero AS

### Task:
Write a RabbitMQ pubsub (publisher/subscriber) program that calculates the moving maximum (running maximum) over 100
samples in (soft) real time of an incoming stream of signed 64-bit integers.
Publish your result after processing the incoming number and in addition forward the incoming number to the verifying node.

Think about how this can be made memory and compute efficient.

Add documentation and further adjustments as you see fit.

A rough guide to getting started can be found below.

Have fun, don't stress and good success :)

#### Requirements

* A docker-compose installation. Please see the [docker-compose installation instructions](https://docs.docker.com/compose/install/) for more information.
* A programming language of your choice with a RabbitMQ client (and preferably a JSON library as well). Please refer to the [RabbitMQ Client Libraries and Developer Tools](https://www.rabbitmq.com/devtools.html).

#### Steps:

1. Implement a small program with a RabbitMQ pubsub client that computes the maximum value over a running window of 100 consecutive samples. [Topics and message format](#topics-and-message-format)
describes the topics (data channels) in use, and the message structure you're expected to use.
2. When you're ready to test your solution, spin up the `docker-compose`. Please see more instructions in [Testing your solution](#testing-your-solution).
3. Open the CSV file placed under *results/results.csv* and check that all fields in the rightmost column are `true`.
4. Send your solution and the csv to the maintainers.

## Topics and message format

The `docker-compose` in this challenge hosts a RabbitMQ broker, a random number generator and a validator script. These
components use two different topics, that you're expected to consume from and publish to. They are, respectively:


### rand

`rand` - The random number generator publishes messages to this topic. You are expected to subscribe to and consume
these messages in your program. The messages are JSON formatted and contains a `sequence_number` and a `rand` field, like
so:

```json
{
  "sequence_number": 0,
  "rand": 25
}
```

### solution

`solution` - The validator consumes messages from this topic. You are expected to publish the your results on this
topic. The messages published to this topic must be JSON formatted and contain a `sequence_number`, `rand` and
`running_max` field. **You should not change the value of `sequence_number` and `rand` in your program.** Example message:

```json
{
  "sequence_number": 2373,
  "rand": 25,
  "running_max": 12947712
}
```

## Testing you solution

When you're ready to test your solution, you should use the `docker-compose` provided in the repository. Please run:

```bash
docker-compose up -d # starts the docker-compose services and begins producing messages
# wait a second or two
docker-compose ps # ensure that the rabbitmq and validator services are "up". The number generator will terminate once it has produced its allocated number of messages.
docker-compose logs -f # Check if the rabbitmq broker is up and the other services have `CONNECTED`

# run your own solution - you'll know better what to do here (hopefully)
```


#Running the solution (Max Compute)
In the root of this directory run `python receiver/RunningMaxComputer.py`


It is a good idea to stop the `docker-compose` when you have tested your script, as it will restart the containers on every boot of your machine.
Unless you specify a `NUMBER_OF_MESSAGES` environment variable in the docker-compose it will produce messages for ever.

Please do so by running:

```bash
docker-compose down
```

### Starting only RabbitMQ

In some cases it can be beneficial to only run RabbitMQ to test your connection. You may do so by running:

```bash
docker-compose up -d rabbitmq
```

## License:
Copyright (C) 2015 General Interfaces GmbH

Copyright (C) 2020 Aivero AS

Maintainer: Tobias Morell, Raphael Dürscheid

Program: *Challenge the coder*

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


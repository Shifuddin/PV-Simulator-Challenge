# PV-Simulator-Challenge

## Project Description
This project illustrates the pub-sub process by implementing a scenario of home power consumption. It constitute of three major modules name Meter, broker, and PV Simulator. Finally, data, power consumption, are stored in a file.

### Meter: 
This should produce messages to the broker with random but continuous values from 0 to 9000 Watts. This is to mock a regular home power consumption.

### PV simulator: 
It must listen to the broker for the meter values, generate a simulated PV power value and the last step is to add this value to the meter value and output the result.

### Writing to a file:
We want the result to be saved in a file with at least a timestamp, meter power value, PV power value and the sum of the powers (meter + PV). The period of a day with samples every couple of seconds would be enough.

## How to run
To run this project, you need to have **docker** installed in your machine. A **docker-compose** file starts up all the services. Services includes meter, rabbitmq, and pv-simulator.

### Configurations
Configurations are adjusted in the **docker-compose** file. Please change if it's necessary.

* min_pv: Minimum Power Value.
* max_pv: Maximum Power Value.
* publishing_interval_seconds: publishing interval of the Meter in seconds.
* initial_delay_second_for_broker_startup: Intial delay for the broker connection.
* broker_address: Full address of the broker.
* broker_msg_queue: Message Queue of the broker.
* filestore: Output file.
* logfile: Log file. 


### Steps
 1. `docker-compose build` (to build the images)
 2. `docker-compose start` (start the services)
 3. `docker-compose stop` (stop the services)
 
 ## Output
 ### Logs
 Please find the respective log files in **meter/log** and **pv_simulator/log/** directories.
 ### PV Output
 Please find the pv output file as **pv_simulator/log/pv.csv**
 ### UI
 Please visit http://localhost:15672 to have look at the broker.

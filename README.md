# SwitchDin Skills Test | MQTT Publish - Subscribe Implementation using Python
Repository to hold SwitchDin Skills Test | Implementation of a MQTT Publish Subscribe system with three clients in total.

### Python Modules Required to run the program:
- paho
- schedule
- prettytable

### Overview of Source Code:
 `client-publisher.py` : This MQTT Client connects to the broker and publishes a Random Number between 1 and 100 at random intervals between 1 and 30 seconds to the topic `switchDin/randomNumber`

`client-sub-1.py` : This MQTT Client connects to the broker and subscribes to the topic `switchDin/randomNumber` and then calculates 1 minute, 5 minute and 30 minute averages and publishes it back to the MQTT broker on the various subtopics in `switchDin/stats/` topic.

`client-sub-2.py` : This MQTT Client connects to the broker and subscribes to the the various subtopics in `switchDin/stats/` topic. Then prints the averages in a table on the console generated using the `prettyTable` python module. 


### How to Run?
- Ensure correct address of MQTT Broker added to each source code. Default value: Local Host
- Run each python file in a terminal after installing the modules listed above. Make sure the python files are ran in the following order:
	- `client-publisher.py`
	- `client-sub-1.py`
	- `client-sub-2.py`

***The following is how the program should look like :***
![enter image description here](https://i.imgur.com/ewCQ1bf.png)



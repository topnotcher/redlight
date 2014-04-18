#What the hell is this???#
This is perhaps the most awesome use of shinken (or nagios) notifications ever. 

Notifications from shinken are sent out via an HTTP request to a Raspberry Pi. When a service enters the CRITICAL state (or DOWN for host), a [flashing red police light](http://www.amazon.com/Rhode-Island-Novelty-Police-Beacon/dp/B0011CZV5A/ref=sr_1_1) connected to the Pi via solid state relay is activated. The light remains on until another state notification is received, or a 30 minute timeout expires. In shinken, the light can be configured just like any other notification way: it can be set to turn on only during workhours, assigned to various contacts, etc. 

#Why?#
- I was bored.
- For the lolz.


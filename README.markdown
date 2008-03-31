Portfolio
=========

This is my portfolio repository. It contains the following projects:

bugs
----

A TurboGears based bugtracker much like trac.

ecAEPS
------

A system for administering the AEPS, which is an assessment given to 
kids that are developmentally disabled. Replaced 
[AEPSi](http://www.aepsinteractive.com/index.htm) for the UO

googleauth
----------

A [drupal](http://drupal.org) plugin that exposes a SAML server 
specifically for use with Google Apps for Education -- this was a Google 
Summer of Code (2007) project

Guildr
------

A TurboGears project that allows people to form guilds across many sites 
that track various meaningful statistics in order to facilitate the 
creation of communities around them.

OpenID
------

I claim that this project is the first opensource OpenID server that 
actually works. I was thrashing around trying to find a working OpenID 
server at 2 in the morning the day of the first coding sprint that the 
University of Oregon's ACM student club was running, and could find 
nothing that worked out of the box, so I wrote this. It requires the 
python JanRain OpenID libraries, SQLObject, and Kid.

Whitepages
----------

I hacked up a quick whitepages search tool for the University of Oregon. 
The problem was that the Qwest website for searching the whitepages was 
not working at all well under safari. I downloaded the individual 
phonebook pages (they're available as .swf), used swfdump to extract the 
text. Then, I wrote a python script to extract the useful information 
out of the dump and place it in a MySQL database. The cgi script then 
presents this information in a useful manner.

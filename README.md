# Proto of C2 server for education
=================

Here is my example of writing C2 server and malware.

## bot_server.py
Here is a server bot with mysql config example.
It also uses serv.py as API for registrating computers.

## serv.py
Register new computers in web.

## tele_test.py
Example of telegram bot for viewing info about infected computers. Already has api token.

## schema.sql
Use for fast creation of mysql db.

## proxy_server.py
Useless now, BUT
* TODO: make this for proxy traffic from client to sites via infected computers.

## server_legacy.py
Do not worry, this is just a client for C2.
Awfull, I know, but one day I will beautify it.

## feedback.py
It has to be in infection folder, but we have what we have. Sends logs from infected computer to another special server.

## down (folder)
files, which has to be uploaded to computer

## c2c (folder)
Depricated chimera

## site (folder)
The only thing you have to know, that client_loader.py has to be delivered to a computer and has to be started.
It downloads from server files for infection (simple loader).
* TODO: make a Starter to run files in multiprocess

## test (folder)
Nothing interesting, here I test modules for infectioning

## tmp_up (folder)
There are files, which are downloaded by client_loader.py (modules).
### tmp (folder)
folder for testing modules
### legend (folder)
script for interacting with infected computer via client
### Postexploit_modules (folder)
* All files are understandable by name
* BUT:
*   s.py has to be a script for making virus runs, when computer wakes up
*   side_encryptor.py is a smth very good encryptor, which I stole from smbd and do not use (use encryptor.py (even if it is weak (will be improved)))

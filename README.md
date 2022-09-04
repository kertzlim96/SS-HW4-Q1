## SS-HW4-Q1
 Systems Security HoneyWords Implementation


## Assignment Requirements
The HoneyWords [2] aims to enhance protection of password-based authentication systems. Design and implement (in any language) a simple version of HoneyWords [1]. Your implementation should have at least the following features:
• Create new accounts
• Authenticate to the front-end server by sending their (username, password) pairs.
• Raise an alarm on detection of malicious logins (i.e., when there is evidence that an incorrect, cracked, password is used).
Communication between entities in your system must be done over TCP. Demonstrate that the system works, and analyse its security. (Keep in mind that an adversary knows how your system works internally.)

https://people.csail.mit.edu/rivest/pubs/JR13.pdf


## The Chaffing-with-a-password-model method from the paper is implemented:

This method generates honeywords using a probabilistic model of real passwords. In this project, a "10k-most-common.txt" wordlist is used.
When a new user registers an account, the actual password and 9 random honeywords from the wordlist are shuffled and added into the password database.
When an attacker tries to log in using a honeyword (possibly as a result of a dictionary attack), an alert will be triggered.


## How to run

  1. Install flask for Python 2.7: 

pip install flask

  2. Run the webserver with the generation method given as argument: 

python webserver.py

  3. Using a web browser, navigate to http://127.0.0.1:5000

  4. To register an account, click on "Create an account" and type in a username and password

  5. Log in using the newly registered credentials
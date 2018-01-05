A slack bot that checks to see if you performed a daily commit in the github repository.
I tested it on Ubuntu 14.04.

## Install python package
```
pip install github3.py
```

## Usage
```
1. git clone https://github.com/jhhwang4195/commitbot.git

2. Modify the token variable value to API Token value for bot
ex) token = 'API token for your bot'  ---> xoxb-293139319120-sYvryaz7WEwYaJFOfZOdoBKU

3. Modify the members github account, repository, and name.
ex) ('jhhwang4195', 'TIL', 'jhhwang')

4. python main.py

5. Example Results 
A bot that checks daily commits.
jhhwang commited today.
sylee has not committed for 18 days.
```

## Reference
* https://github.com/hyesun03/commit-bell/blob/master/commit-bell.py

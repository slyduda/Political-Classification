#Should contain the user path for authorization. Will be replaced by a param script.
path = 'C:\\Users\\fk339sq\\Documents\\Git Secrets\\Twitter App.txt'
contents = ""
with open(path, 'r') as f:
    contents = f.readlines()

new_contents = []
for line in contents:
    line = line.rstrip('\n')
    new_contents.append(line)

CONSUMER_KEY=new_contents[0]
CONSUMER_SECRET=new_contents[1]
ACCESS_TOKEN_KEY=new_contents[2]
ACCESS_TOKEN_SECRET=new_contents[3]
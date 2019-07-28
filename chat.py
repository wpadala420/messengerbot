import fbchat
from Levenshtein import jaro_winkler

DANGEROUS = ['jaranie', 'blancix', 'temat', 'jarać', 'palto', 'palenie', 'blant', 'pixy', 'dropy', 'marihuana',
             'przypalać', 'skręcę', 'skręcić', 'zawinąć', 'opcji', 'opcje', 'opcję', 'szpontę', 'zawijać', 'sztuka']

DANGEROUS_PEOPLE = ['Jakub Bomba', 'Emil Wróbel', 'Artur Skrabucha', 'Paweł Nagajek', 'Wojciech Ciołek',
                    'Krzysiek Chapski'
    , 'Emil EK', 'Kamil Jóźwik', 'Sebastian Wrzosek', 'Adrian Rafalski']

client = fbchat.Client('vojtekk94@o2.pl', 'kochampalictrawke')
threads_ids = []


threads=client.fetchThreadList()


full_msgs = []
for i in threads:
    if i.name in DANGEROUS_PEOPLE:
        a = client.fetchThreadMessages(i.uid)
        full_msgs.append(a)


msgs_to_delete = []
for i in range(len(full_msgs)):
    flag = False
    for j in range(len(full_msgs[i])):
        if full_msgs[i][j].text:
            words = full_msgs[i][j].text.split(' ')
            for l in words:
                for m in DANGEROUS:
                    if jaro_winkler(l, m) >= 0.8:
                        msgs_to_delete.append(full_msgs[i][j])
                        flag = True
                    if flag:
                        break
                if flag:
                    break


for i in msgs_to_delete:
    client.deleteMessages(i.uid)


test = { 'id': { 'test':'test' }}

another = { 'w':'w' }

test['id'].update(another)

print(test)

test['id'].pop('test')

print(test)
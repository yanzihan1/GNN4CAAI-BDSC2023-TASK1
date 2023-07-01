import json

train_f=open('../data/source_event_preliminary_train_info.json')
valid_f=open('../data/target_event_preliminary_train_info.json')
# test_f=open('../data/target_event_preliminary_test_info.json')

user2id={}
id_=0
########### user2dict的代码####################
line = json.load(train_f)
for lines in line:
    leftuser=lines.get("inviter_id")
    rightuser=lines.get("voter_id")
    if user2id.get(leftuser) is None:
        user2id[leftuser]=id_
        id_+=1
    if user2id.get(rightuser) is None:
        user2id[rightuser]=id_
        id_+=1

line = json.load(valid_f)
for lines in line:
    leftuser=lines.get("inviter_id")
    rightuser=lines.get("voter_id")
    if user2id.get(leftuser) is None:
        user2id[leftuser]=id_
        id_+=1
    if user2id.get(rightuser) is None:
        user2id[rightuser]=id_
        id_+=1
########### user2dict的代码  END####################

####
train_f=open('../data/source_event_preliminary_train_info.json')
valid_f=open('../data/target_event_preliminary_train_info.json')
fw=open('deepwalk_train.list','w')
line = json.load(train_f)
for lines in line:
    leftuser=lines.get("inviter_id")
    rightuser=lines.get("voter_id")
    leftid=user2id.get(leftuser)
    rightid=user2id.get(rightuser)
    fw.write(str(leftid)+' '+str(rightid)+'\n')

line = json.load(valid_f)
for lines in line:
    leftuser=lines.get("inviter_id")
    rightuser=lines.get("voter_id")
    leftid=user2id.get(leftuser)
    rightid=user2id.get(rightuser)
    fw.write(str(leftid)+' '+str(rightid)+'\n')







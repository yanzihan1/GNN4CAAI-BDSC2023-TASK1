import json
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from do_buy_feature.by_feature import get_by_feature
scaler2 = StandardScaler()
#
print("获取消费数据")
user_cost_data=get_by_feature()
# def eventDict():
f=open('data/event_info.json','r')
line=json.load(f)
parent2id={}
even2parentid={}
curId=0
for lines in line:
    event_id=lines.get("event_id")
    parent_event_id=lines.get("parent_event_id")
    if parent2id.get(parent_event_id) is None:
        parent2id[parent_event_id]=curId
        curId+=1
    even2parentid[event_id]=parent2id.get(parent_event_id)
print(len(even2parentid))

def af(ac2id,kinds='node'):
    cloud_user=0
    userdict={}
    outputNodeFeature=[]

    reldict={}
    outputRelFeature=[]

    if kinds=='node':
        f=open('data/user_info.json','r',encoding='utf-8')
        lines=json.load(f)
        for i in lines:
            feature = []
            user_id=i["user_id"]
            gender_id=i["gender_id"]
            age_level=i["age_level"]
            user_level=i["user_level"]
            for i in range(33):
                feature.append(float(gender_id))
            for i in range(33):
                feature.append(float(age_level))
            for i in range(34):
                feature.append(float(user_level))
            if user_cost_data.get(user_id) is None:
                for i in range(56):
                    feature.append(0.0)
                cloud_user+=1
            ########结构数据和时序数据在后面添加
            # if graph_stru.get(user_id) is None:
            #     for i in range(48):
            #         feature.append(graph_stru.get(user_id))
            # if real_time.get(user_id) is None:
            #     for i in range(48):
            #         real_time.get(user_id)
            else:
                for i in user_cost_data.get(user_id):
                    feature.append(float(i)*0.1)
            userdict[user_id]=feature
        print("cloud_user",cloud_user)
        for i,j in ac2id.items():
            outputNodeFeature.append(userdict.get(i))
        outputNodeFeaturenp=np.array(outputNodeFeature)
        outputNodeFeature = scaler2.fit_transform(outputNodeFeaturenp)
        outputNodeFeature=outputNodeFeature*0.01
        outputNodeFeature=outputNodeFeature.tolist()
        return torch.tensor(outputNodeFeature)
    else:
        f=open('data/source_event_preliminary_train_info.json','r',encoding='utf-8')
        lines=json.load(f)
        for i in lines:
            feature = []
            event_id=i["event_id"]
            # if_inviter_participate=float(i["if_inviter_participate"])
            # if_voter_participate=float(i["if_voter_participate"])
            # ds=float(int(i["ds"][-3:])*0.02)
            # user_level=float(i["user_level"])
            # for i in range(33):
            #     feature.append(if_inviter_participate)
            # for i in range(25):
            #     feature.append(if_voter_participate)
            # for i in range(34):
            #     feature.append(ds)
            for i in range(156):
                feature.append(even2parentid.get(event_id))
            reldict[event_id]=feature
        f = open('data/target_event_preliminary_train_info.json', 'r', encoding='utf-8')
        lines = json.load(f)
        for i in lines:
            feature = []
            event_id = i["event_id"]
            # if_inviter_participate = float(i["if_inviter_participate"])
            # if_voter_participate = float(i["if_voter_participate"])
            # user_level=float(i["user_level"])
            # ds=float(int(i["ds"][-3:])*0.02)
            # user_level=float(i["user_level"])
            # for i in range(33):
            #     feature.append(if_inviter_participate)
            # # for i in range(25):
            # #     feature.append(if_voter_participate)
            # for i in range(34):
            #     feature.append(ds)
            for i in range(156):
                feature.append(even2parentid.get(event_id))
            reldict[event_id] = feature
        nf=0
        for i,j in ac2id.items():
            feature2=[]
            if reldict.get(i) is None and '_reverse' in i:
                i=i[:-8]
                if reldict.get(i) is None:
                    # for i in range(33):
                    #     feature2.append(if_inviter_participate)
                    # # for i in range(25):
                    # #     feature2.append(if_voter_participate)
                    # for i in range(34):
                    #     feature2.append(ds)
                    for i in range(156):
                        feature2.append(even2parentid.get(event_id))
                    outputRelFeature.append(feature2)
                    nf+=1
                else:
                    outputRelFeature.append(reldict.get(i))
            elif reldict.get(i) is None:
                # for i in range(33):
                #     feature2.append(if_inviter_participate)
                # # for i in range(25):
                # #     feature2.append(if_voter_participate)
                # for i in range(34):
                #     feature2.append(ds)
                for i in range(156):
                    feature2.append(even2parentid.get(event_id))
                outputRelFeature.append(feature2)
                nf += 1
            else:
                outputRelFeature.append(reldict.get(i))
        outputRelFeaturenp = np.array(outputRelFeature)
        outputRelFeature = scaler2.fit_transform(outputRelFeaturenp)
        outputRelFeature=outputRelFeature*0.01
        outputRelFeature = outputRelFeature.tolist()
        print("没有特征的事件:",nf)
        return torch.tensor(outputRelFeature)
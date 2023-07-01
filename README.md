# GNN4CAAI-BDSC2023-TASK1
### CAAI-BDSC2023社交图谱链接预测 任务一：社交图谱小样本场景链接预测
### 比赛链接:https://tianchi.aliyun.com/competition/entrance/532073/introduction?spm=a2c22.12281925.0.0.7aa47137syzS2r
### 单模复赛: 15  MRR:0.3724
### 比赛思路：

  猜测用DeepFM DNN LGB等方案最后走融合才是前排正解，但是我平时有做一些GNN研究，所以就简单聊聊如何用GNN单模完成这类推荐任务

  ### BaseLine选择：
     主办方用的CompGCN中的mult，ComGCN本身已经是近年的sota之作，所以就沿用了，针对baseline的消融实验如下：
     
| 消融实验 | 作用 | 
| :-----| ----: |
| mult替换为conve方式计算 | $\downarrow$ |
| 扩大layersize和dim |$\uparrow$ |
| 扩大负采样 |$\uparrow$ |
| GCN部分改为SAGE |-|

### 特征融入
    在这里采用了最简单的GCN特征融入方式，替换初始化特征矩阵，具体的分为了结构特征+用户画像+消费特征以及边特征
    - 结构特征：
         1、采用了LINE进行图结构的初始化，输出为128dim，利用pca降低至48dim，记为user_Stru
    - 用户画像：
         2、采用了 Concat (用户的会员等级+年龄+性别)，维度一共为64dim，记为user_fea
    - 消费特征
         3、主要考虑用户的消费行为，这里可以理解为用ComGCN先做了一次训练 节点不是用户-用户； 而是用户-事件，把用户和事件都看作节点，当用户在某一个事件下有过消费行为，就把该用户和该事件进行连边，date是边特征，是用的one-hot初始边特征, 所以同一个用户可以和同一个事件得到多个连边。计算得到用户节点特征user_fea_pre  事件节点特征event_feature_pre,分别为128dim，然后降维至48dim
    #### 节点特征
    节点特征采用 Concat(user_Stru,user_fea,user_fea_pre) 一共160dim
    ###  边特征
    边特征采用 Concat(parent_event_feature(72dim),event_feature_pre) 一共160dim

    特征归一化采用的 StandardScaler.fit_transform
### 其他改动

     1、修改负采样，参考kdd2021 mixgcf论文 很巧妙的设计，有效
     
     2、训练集中包含非常多的非连通图，而包含测试集节点的连通图部分只有一半，删除噪声会导致弱监督情况下W不具有鲁棒性，但是加上又容易造成模型坍塌，所以对不包含测试集节点的连通图做扰动，随机增删边增加弱监督鲁棒性而又不改变正确的传递信息，有效。

函数主文件:main4.py  部分特征文件需要自己运行得到



### 可以考虑的
- 做的很粗糙 仅考虑GNN单模作为参考，很多训练优化方案比如梯度惩罚,fgm,pgd,ema,lookahead,warmup等等防止过拟合 都会更加有效。GNN跑的很慢，我在这儿就都没有做进一步实验了。
- 融合(投票，概率相加等都是有效提分的方案)，因为没时间+跑得慢也没有进一步考虑
- 做为特征方案的其中一种特征，比如放到lgb里面 我认为这才是正确的方案吧

比赛结束很高兴分享这个方案和大家一起讨论GNN的学习，有疑惑的可以发邮件:yzhcqupt@163.com，我会在这两天把代码整理好share出来




  

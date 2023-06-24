# GNN4CAAI-BDSC2023-TASK1
### CAAI-BDSC2023社交图谱链接预测 任务一：社交图谱小样本场景链接预测
### 比赛链接:https://tianchi.aliyun.com/competition/entrance/532073/introduction?spm=a2c22.12281925.0.0.7aa47137syzS2r
### 单模复赛: 14
### 比赛思路：

  猜测用DeepFM DNN LGB等方案最后走融合才是前排正解，但是我想试一试用纯GNN做出来是什么样子，所以就简单聊聊如何用GNN完成这类推荐任务

  ### BaseLine选择：
     主办方用的CompGCN中的mult，ComGCN本身已经是近年的sota之作，所以就沿用了，针对baseline的消融实验如下：
     
| 消融实验 | 作用 | 
| :-----| ----: |
| mult替换为conve方式计算 | $\downarrow$ |
| 扩大layersize和dim |$\uparrow$ |
| 扩大负采样 |$\uparrow$ |


  

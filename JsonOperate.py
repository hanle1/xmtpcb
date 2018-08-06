import json
from datetime import *
import time
import random
import os
import sys
sys.setrecursionlimit(100000) #例如这里设置为十万
from hdfs.client import Client
class JsonOperate():
    errlist = []
    result = []
    def eachFile(self,filepath):
        i = 0
        g = os.walk(filepath)
        for path, d, filelist in g:
            for filename in filelist:
                if os.path.splitext(filename)[1] == ".json":  # 判断是否是txt
                    if os.path.split(filename)[1].split('.')[0] != 'PanelCheck' and  os.path.split(filename)[1].split('.')[0].find('bad') < 0:
                        self.result.append(os.path.join(path, filename))
        l = len(self.result)
        for path in self.result:
            i = i+1
            print(path+'...'+ str(i) +'..in..' + str(l))
            self.json_format_to_hdfs(filename=path)
        # pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回List
        # for s in pathDir:
        #     newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        #     if os.path.isfile(newDir):  # 如果是文件
        #         if os.path.splitext(newDir)[1] == ".json":  # 判断是否是txt
        #             if os.path.split(newDir)[1].split('.')[0] == 'PanelCheck':
        #                 print('hello')
        #             else:
        #                 self.json_format_to_hdfs(filename=newDir)
        #     else:
        #         self.eachFile(filepath=newDir)  # 如果不是文件，递归这个文件夹的路径

    def random_id(self):
        for i in range(0, 1):
            nowTime = datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前的时间
            randomNum = random.randint(0, 100)  # 生成随机数n,其中0<=n<=100
            if randomNum <= 10:
                randomNum = str(0) + str(randomNum)
            uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def __init__(self, format_data_path):
        self.format_data_path = format_data_path

    def json_format_to_hdfs(self,filename):
        random_id = self.random_id()
        newpilepath = './' + random_id + '.json'
        with open(filename, 'r+',encoding="ISO-8859-1") as f:
            content = f.read()
            with open(newpilepath,'w') as a:
                a.seek(0, 0)
                a.write('[' + content + ']')
        with open(newpilepath,'r') as a:
            print(newpilepath)
            try:
                pop_data = json.load(a)
            except Exception:
                self.errlist.append(filename)
                pop_data='error'
        if pop_data == 'error' :
            return
        with open(newpilepath,'w') as a:
            a.truncate()
        with open(newpilepath, 'a') as a:
            for pop_dict in pop_data:
                stationCode = pop_dict['stationCode']
                if 'deviceId' in pop_dict:
                    pop_dict[stationCode + '_deviceId'] = pop_dict['deviceId']
                    del pop_dict["deviceId"]
                pop_dict[stationCode + '_result'] = pop_dict['result']
                pop_dict[stationCode + '_errorCode'] = pop_dict['errorCode']
                pop_dict[stationCode + '_info'] = pop_dict['info']
                pop_dict[stationCode + '_tbTag'] = pop_dict['tbTag']
                if 'singleTag' in pop_dict:
                    pop_dict[stationCode + '_singleTag'] = pop_dict['singleTag']
                    del pop_dict["singleTag"]
                pop_dict[stationCode + '_workOrder'] = pop_dict['workOrder']
                pop_dict[stationCode + '_date'] = pop_dict['date']
                pop_dict[stationCode + '_time'] = pop_dict['time']
                time = pop_dict['time']
                if (83000 < int(time) < 203000):
                    pop_dict[stationCode+'_time_cnt_num'] = 1
                else:
                    pop_dict[stationCode+'_time_cnt_num'] = 0
                del pop_dict["result"]
                del pop_dict["errorCode"]
                del pop_dict["info"]
                del pop_dict["tbTag"]
                del pop_dict["workOrder"]
                del pop_dict["date"]
                del pop_dict["time"]
                json_str = json.dumps(pop_dict, ensure_ascii=False)
                a.write(json_str + '\n')
        with open(newpilepath,'r') as a:
            data = a.read()
            # string = json.dumps(data,ensure_ascii=False)
        url = "http://10.141.212.26:50070"
        client = Client(url, root=None, proxy=None, timeout=None, session=None)
        path = self.format_data_path + stationCode
        if not os.path.exists(path):
            os.mkdir(path)
        with open(self.format_data_path + stationCode + '/' + stationCode + '.json', 'a+') as f:
            f.write(data)
        os.remove(newpilepath)
def main():
    json = JsonOperate("/Users/apple/workspaces/fudan/data/format_data/")
    json.eachFile(filepath="/Users/apple/workspaces/fudan/data/S01")
    print(json.errlist)
if __name__ == "__main__":
    main()

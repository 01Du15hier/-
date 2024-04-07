# 开发者：远渡
# 开发时间：2022/4/13 20:25
import pymysql
import pandas
import time
import re



def menu():
    print('====================学生信息管理系统====================')
    print('-----------------------功能菜单------------------------')
    print('1.查看规则'.center(40,' '))
    print('2.添加规则'.center(40, ' '))
    print('3.查看原子命题代号'.center(40, ' '))
    print('4.添加原子命题代号'.center(40, ' '))
    print('5.查看匹配库'.center(40, ' '))
    print('6.精确推理'.center(40, ' '))
    print('7.模糊推理'.center(40, ' '))
    print('0.退出系统'.center(40, ' '))
    print('-----------------------功能菜单------------------------')
    print('=====================================================')


def IP_judge(ip):#IP地址合法性判断函数
    pattern=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')#re正则匹配IP地址
    if pattern.match(ip):
        return True
    else:
        return False

def Port_judge(port):#端口合法性判断函数
    if port in range(0,65536):
        return True
    else:
        return False

def DB_connection():
    global HOST
    global PORT
    global USER
    global PASSWD
    while 1:
        while 1:
            HOST=input('请输入主机IP地址，默认127.0.0.1\n')
            if HOST=='':
                HOST='127.0.0.1'
                break
            else:
                if IP_judge(HOST):#检测用户输入的IP是否有效
                    break
                else:
                    print('目标主机地址无效，请重新输入')
                    continue
        while 1:
            PORT=input('请输入MySQL数据库端口号，默认3306\n')
            if PORT=='':
                PORT=3306
                break
            else:
                if Port_judge(PORT):
                    PORT=int(PORT)
                    break
                else:
                    print('设置端口无效，请重新输入')
                    continue
        while 1:
            USER=input('请输入数据库登录用户名，默认root\n')
            if USER=='':
                USER='root'
                break
            else:
                break
        while 1:
            PASSWD=input('请输入对应密码\n')
            if PASSWD=='':
                print('请输入密码')
                continue
            else:
                break
        try:#检测能否连接数据库
            connetion1=pymysql.connect(host=HOST,port=PORT,user=USER,password=PASSWD,db='rule')
            connetion2=pymysql.connect(host=HOST,port=PORT,user=USER,password=PASSWD,db='rule_match')
            connetion3=pymysql.connect(host=HOST,port=PORT,user=USER,password=PASSWD,db='atomic_proposition')
            connetion1.close()
            connetion2.close()
            connetion3.close()
            break
        except:
            print('数据库连接错误，请检查信息是否正确')
            time.sleep(3)
            continue


def getPremises(rule_num):#获取推理的条件
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')  # 本地连接数据库
    cursor = connetion.cursor()  # 创建一个游标对象，因为用大蟒蛇操作海豚需要用到游标
    DB_list = []
    for i in range(1,9):
        SQL_sentence="select "+"premise"+str(i)+' from rule where rule_num='+rule_num+";"
        cursor.execute(SQL_sentence)
        result_tuple = cursor.fetchall()
        for j in result_tuple:#双层括号去除
            for k in j:
                if k is not None:#为了规则库后续的升级，故额外预备了列，多余的列存放NULL，通过Python得到时为None
                    DB_list.append(k)
    return DB_list


def Comparison(DB_list,user_list,rule_num='0'):#将用户输入的前提条件与规则库的premises比较
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')
    user_list_backup=[]
    conclusion_list=[]
    for i in user_list:#比较前先查重
        if i not in user_list_backup:
            user_list_backup.append(i)
    count_1=0
    for j in DB_list:#遍历DB_list中的每一个元素，如果该元素在user_list_backup中，则count+1
        if j in user_list_backup:
            count_1=count_1+1
    if len(DB_list)==count_1:#如果DB_list中的每一个元素在user_list_backup中都能找到，则查询规则库得到对应结论
        SQL_sentence ="select conclusion from rule where rule_num="+rule_num+";"
        cursor = connetion.cursor()
        cursor.execute(SQL_sentence)
        result_tuple = cursor.fetchall()
        for i in result_tuple:#双层括号去除
            for j in i:
                conclusion_list.append(j)
        cursor.close()  # 关闭游标以免干扰下次查询
    return conclusion_list


def confirmation(user_list):#用于验证用户输入的原子命题是否存在
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')
    count=0
    FLAG=0#立个旗杆，0表示未完成原子命题存在确认，1表示完成原子命题存在确认
    for i in range(len(user_list)):
        SQL_sentence = "select Atomic_proposition_num from Atomic_proposition where Atomic_proposition_num="+user_list[i]
        cursor = connetion.cursor()
        cursor.execute(SQL_sentence)
        result_tuple = cursor.fetchall()
        cursor.close()  #关闭游标以免干扰下次查询
        if result_tuple != ():  # 获得的元组不为空则说明用户输入的此原子命题存在与原子命题代库中
            count+=1
            continue
        else:
            print('请输入存在于原子命题库中的原子命题代号')
            print('输入的原子命题'+user_list[i]+'不存在请重新输入')
            return FLAG
    if count==len(user_list):
        FLAG=1
        return FLAG


def logical_reasoning(mode,*u_list):#精确逻辑推理
    while 1:
        if mode==1:#直接精确逻辑推理
            while 1:
                s=input('请输入原子命题代号，各代号之间用英文逗号隔开。退出精确推理请输入quit或exit\n')
                if s.lower()=='quit' or s.lower()=='exit':
                    return
                s_FLAG=1#默认通过
                for individual in s:
                    if (individual.isdigit()==False) and (individual!=','):
                        s_FLAG=0
                        print('请不要输入无关字符')
                        break
                if s_FLAG==0:
                    continue
                user_list=list(s.split(','))
                FLAG=confirmation(user_list)
                if FLAG==0:#FLAG为0，说明原子命题不存在，需要用户重新输入
                    print('请不要输入不存在的原子命题')
                    continue
                else:
                    break
        elif mode==0:#间接精确逻辑推理
            user_list=u_list[0]#获得外部传递过来的列表,此时列表会作为元组的第一个元素,如(['1', '2'],)之类的
            #由于已经在模糊推理中鉴定了原子命题在数据库中存在，此处不再重新验证原子命题存在性
        match_tuple=Match(1)
        list1=match_tuple[0]
        list2=match_tuple[1]
        list3=match_tuple[2]
        list4=match_tuple[3]
        list5=match_tuple[4]
        list6=match_tuple[5]
        list7=match_tuple[6]
        list8=match_tuple[7]
        Conclusion_list1 = []#用于声明局部变量，不能删除
        Conclusion_list2 = []
        Conclusion_list3 = []
        Conclusion_list4 = []
        Conclusion_list5 = []
        Conclusion_list6 = []
        Conclusion_list7 = []
        Conclusion_list8 = []
        for i in list1:#第一轮匹配，匹配前提条件只有一个的规则
            DB_list1=getPremises(i)#得到推理的前提，以列表形式返回了从数据库查询到的premises
            if Comparison(DB_list1, user_list, i) != []:
                Conclusion_list1.extend(Comparison(DB_list1, user_list, i))#用列表扩展方式收集Comparison()传递过来的列表,不能直接赋值,直接赋值会导致后面的覆盖前面的
            for ii in Conclusion_list1:#遍历conclusion_list1，如果ii不在user_list里，则将ii加入user_list。即将推理出来的结论转变为前提条件
                if ii not in user_list:
                    user_list.append(ii)

        for j in list2:#第二轮匹配，匹配前提条件只有两个的规则
            DB_list2=getPremises(j)
            if Comparison(DB_list2, user_list, j) != []:
                Conclusion_list2.extend(Comparison(DB_list2, user_list, j))
            for jj in Conclusion_list2:#遍历conclusion_list2，如果jj不在user_list里，则将jj加入user_list。即将推理出来的结论转变为前提条件
                if jj not in user_list:
                    user_list.append(jj)
        for k in list3:  #第三轮匹配，匹配前提条件只有三个的规则
            DB_list3 = getPremises(k)
            if Comparison(DB_list3, user_list, k) != []:
                Conclusion_list3.extend(Comparison(DB_list3, user_list, k))
            for kk in Conclusion_list3:#遍历conclusion_list3，如果kk不在user_list里，则将kk加入user_list。即将推理出来的结论转变为前提条件
                if kk not in user_list:
                    user_list.append(kk)

        for l in list4:#第四轮匹配，匹配前提条件只有四个的规则
            DB_list4=getPremises(l)
            if Comparison(DB_list4, user_list, l)!=[]:
                Conclusion_list4.extend(Comparison(DB_list4, user_list, l))
            for ll in Conclusion_list4:#遍历conclusion_list4，如果ll不在user_list里，则将ll加入user_list。即将推理出来的结论转变为前提条件
                if ll not in user_list:
                    user_list.append(ll)
        for m in list5:#第五轮匹配，匹配前提条件只有五个的规则
            DB_list5=getPremises(m)
            if Comparison(DB_list5, user_list, m) != []:
                Conclusion_list5.extend(Comparison(DB_list5, user_list, m))
            for mm in Conclusion_list5:#遍历conclusion_list5，如果mm不在user_list里，则将mm加入user_list。即将推理出来的结论转变为前提条件
                if mm not in user_list:
                    user_list.append(mm)
        for n in list6:#第六轮匹配，匹配前提条件只有六个的规则
            DB_list6=getPremises(n)
            if Comparison(DB_list6, user_list, n) != []:
                Conclusion_list6.extend(Comparison(DB_list6, user_list, n))
            for nn in Conclusion_list6:#遍历conclusion_list6，如果nn不在user_list里，则将nn加入user_list。即将推理出来的结论转变为前提条件
                if nn not in user_list:
                    user_list.append(nn)
        for o in list7:#第七轮匹配，匹配前提条件只有七个的规则
            DB_list7=getPremises(o)
            if Comparison(DB_list7, user_list, o) != []:
                Conclusion_list7.extend(Comparison(DB_list7, user_list, o))
            for oo in Conclusion_list7:#遍历conclusion_list7，如果oo不在user_list里，则将oo加入user_list。即将推理出来的结论转变为前提条件
                if oo not in user_list:
                    user_list.append(oo)
        for p in list8:#第八轮匹配，匹配前提条件只有八个的规则
            DB_list8=getPremises(p)
            if Comparison(DB_list8, user_list, p) != []:
                Conclusion_list8.extend(Comparison(DB_list8, user_list, p))
            for pp in Conclusion_list8:#遍历conclusion_list8，如果pp不在user_list里，则将pp加入user_list。即将推理出来的结论转变为前提条件
                if pp not in user_list:
                    user_list.append(pp)
        conclusion_list_initialization=Conclusion_list1+Conclusion_list2+Conclusion_list3+Conclusion_list4+Conclusion_list5+Conclusion_list6+Conclusion_list7+Conclusion_list8
        conclusion_list=list(set(conclusion_list_initialization))#列表去重
        print('结论编号',conclusion_list)
        connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')
        cursor = connetion.cursor()
        print('结论含义:')
        for conclusion in conclusion_list:
            SQL = "select meaning from atomic_proposition where Atomic_proposition_num=" + conclusion + ";"
            cursor.execute(SQL)
            result_tuple = cursor.fetchall()
            for tuple1 in result_tuple:
                for ele in tuple1:
                    print(conclusion+':'+ele)

        if mode==1:  #直接精确逻辑推理
            answer=input('是否继续精确推理?(Y/N)\n')
            if answer.lower()=='y' or answer.lower()=='yes':
                continue
            elif answer.lower()=='n' or answer.lower()=='no':
                time.sleep(0.5)
                return conclusion_list
            else:
                return conclusion_list
        else:
            return conclusion_list


def fuzzy_reasoning():#模糊推理
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')
    while 1:
        while 1:
            print('请输入关键词，各关键词之间用英文逗号隔开')
            print('百分号%表示匹配任意字符任意次，下划线_表示匹配单个字符')
            print('例如：%feathe_,_ood_at_flyin_')
            print('退出模糊推理请输入quit或exit')
            user_list=input()
            if user_list.lower()=='quit' or user_list.lower()=='exit':
                return
            user_list=list(user_list.split(','))
            for element in user_list:
                for ch in element:
                    if ((ch.isalpha()) or (ch=="'") or (ch=="_") or (ch=="%"))==False:
                        print("关键词中仅允许出现单引号'、下划线_和百分号%,各关键词之间用英文逗号隔开")
                        continue
            break
        while 1:
            user_confirmed = []
            for element in user_list:
                SQL_sentence = 'select meaning from Atomic_proposition where meaning like "' + element + '";'#由于准许了用户输入特殊符号'，SQL语句的引号位置必须特定，不能随意更改
                # 由于模糊查询存在不准确性，故需要将查询到的结果返回呈现给用户进行下一步确认
                cursor = connetion.cursor()
                cursor.execute(SQL_sentence)
                result_tuple = cursor.fetchall()
                cursor.close()#关闭游标以免干扰下次查询
                keyword_replace = 0  # 默认用户未更换关键词
                if result_tuple != ():#若匹配到了，则加入user_confirmed
                    for i in result_tuple:
                        for j in i:
                            user_confirmed.append(j)
                else:
                    while 1:
                        answer1 = input("关键词  " + element + "  未在数据库中得到匹配,请选择Y更换关键词或N放弃该关键词\n")
                        if answer1 == 'Y' or answer1=='y':  # 用户选择更换关键词
                            update = input('请输入新关键词\n')
                            FLAG=1#默认通过
                            for ch in update:
                                if ((ch.isalpha()) or (ch=="'") or (ch=="_") or (ch=="%"))==False:
                                    FLAG=0
                            if FLAG==1:
                                user_list[user_list.index(element)] = update
                            else:
                                print('请不要乱输入!')
                                continue
                            keyword_replace = 1  # 表示用户更换了关键词
                            break
                        elif answer1 == 'N' or answer1 == 'n':  # 用户选择放弃关键词
                            del user_list[user_list.index(element)]
                            break
                        else:
                            print('请不要乱输入')
                            continue
                if keyword_replace == 1:  # 如果更换了关键词，停止遍历user_list中的元素
                    break
                elif keyword_replace == 0:  # 如果未更换关键词，则继续遍历user_list中的元素
                    continue
            if keyword_replace == 1:  # 如果更换了关键词，则返回上一步user_confirmed
                continue
            elif keyword_replace == 0:  # 如果未更换关键词，则中断循环，直接进行下一步
                break
        confirmed_FLAG=0
        while 1:
            print("请进一步确认信息")
            print("以下查询到的关键词，若不是您所需要的，请将它们输入进控制台,我们将放弃这些关键词，再为您进行模糊推理")
            print("如果均为您所需要的，请输入'confirmed'!")
            print("如果您认为有太多关键词不符合您的要求，请输入'Exit'放弃模糊推理")
            print(user_confirmed)
            choice_FLAG = 0
            choice = list(input('请输入您的选择\n').split(','))
            for c in choice:
                if type(c)==str:
                    if c.lower() =='confirmed':
                        confirmed_FLAG = 1 #表示已确认
                        choice_FLAG = 1 #表示选择结束
                        break
                    elif c.lower()=='exit':
                        print('已退出模糊查询')
                        return
                    elif c in user_confirmed:
                        del user_confirmed[user_confirmed.index(c)] #找到该元素索引并通过索引删除它
                        choice_FLAG=1
                        confirmed_FLAG = 1
                    else:
                        print('请不要乱输入')
                        choice_FLAG = 0
                        break
                else:
                    print('请不要乱输入')
                    choice_FLAG = 0
                    break
            if choice_FLAG==0:#选择未结束则继续循环，用于防止用户乱输入
                continue
            else:
                break
        proposition_list=[]
        if confirmed_FLAG==1:
            for k in user_confirmed:
                cursor = connetion.cursor()
                SQL_sentence='select Atomic_proposition_num from Atomic_proposition where meaning="'+k+'";'#通过meaning查Atomic_proposition_num
                cursor.execute(SQL_sentence)#数据库字段中有引号等特殊字符，需要通过叠加引号再加工
                result_tuple = cursor.fetchall()
                cursor.close()  #关闭游标以免干扰下次查询
                for ii in result_tuple:
                    for jj in ii:
                        proposition_list.append(jj)
        return_result_list = logical_reasoning(0, proposition_list)
        #return return_result_list
        print(return_result_list)

        answer=input('是否继续模糊推理(y/n)')
        if answer.lower()=='y' or answer.lower()=='yes':
            continue
        elif answer.lower()=='n' or answer.lower()=='no':
            break
        else:
            print('请不要乱输入')
            break


def show_Atomic_proposition_code(mode):#展示原子命题库给用户看
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')  # 本地连接数据库
    cursor = connetion.cursor()  # 创建一个游标对象，因为用大蟒蛇操作海豚需要用到游标
    cursor.execute("select * from atomic_proposition;")  # 查询结果以元组形式返回
    result_tuple = cursor.fetchall()
    cursor.close()  #关闭游标以免干扰下次查询
    result = pandas.DataFrame(result_tuple)#pandas库DataFrame规范化显示数据库数据
    result.columns = ['Atomic_proposition_num', 'meaning']
    print(result)
    connetion.close()
    if mode==1:
        pass
    elif mode==2:
        while 1:
            answer=input('输入y返回功能菜单\n')
            if answer.lower()=='y' or answer.lower()=='yes':
                break
            else:
                print('请不要乱输入')
                continue
    else:
        print('展示匹配库失败,返回功能菜单')


def show_rules(mode):#展示规则给用户看
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')  # 本地连接数据库
    cursor = connetion.cursor()  # 创建一个游标对象，因为用大蟒蛇操作海豚需要用到游标
    cursor.execute("select * from rule;")  # 查询结果以元组形式返回
    result_tuple = cursor.fetchall()
    cursor.close()  #关闭游标以免干扰下次查询
    result = pandas.DataFrame(result_tuple)#pandas库DataFrame规范化显示数据库数据
    result.columns = ['rule_num', 'conclusion','premise1','premise2','premise3','premise4','premise5','premise6','premise7','premise8']
    print(result)
    connetion.close()
    if mode == 1:
        pass
    elif mode == 2:
        while 1:
            answer = input('输入y返回功能菜单\n')
            if answer.lower()=='y' or answer.lower()=='yes':
                break
            else:
                print('请不要乱输入')
                continue
    else:
        print('展示匹配库失败,返回功能菜单')


def show_rule_match():
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule_match')  # 本地连接数据库
    cursor = connetion.cursor()
    cursor.execute("select * from rule_match order by match_round;")
    result_tuple = cursor.fetchall()
    cursor.close()  #关闭游标以免干扰下次查询
    result = pandas.DataFrame(result_tuple)  # pandas库DataFrame规范化显示数据库数据
    result.columns =['match_round','rule_num']
    print(result)
    connetion.close()
    while 1:
        answer=input('输入y返回功能菜单\n')
        if answer.lower()=='y' or answer.lower()=='yes':
            break
        else:
            print('请不要乱输入')
            continue


def add_rules():#添加规则
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')  # 本地连接数据库
    while 1:
        show_rules(1)  # 展示规则库给用户看
        print('----------添加规则----------')
        print('PS.')
        print("1.规则与规则之间用破折号'-'隔开")
        print("2.结论与前提条件之间用逗号','隔开")
        print("3.结论与结论、前提条件与前提条件之间用空格' '隔开")
        print('4.一条规则仅允许有一条结论;如出现推理出多条结论，请另开多条规则')
        print('例如:  100,88 99表示原子命题88和99可推出结论100')
        string=input('请输入要添加的规则,退出规则添加请输入quit或exit\n')
        if string.lower()=='quit' or string.lower()=='exit':
            connetion.close()
            return
        format_FLAG =1 #默认格式验证通过
        list_rules=string.split('-')
        for rule in list_rules:
            conclusion_list=[]
            backup_list=rule.split(',')
            if len(backup_list)==2:#如果一条规则仅有结论和前提条件两个元素则执行如下代码
                if backup_list[0].isdigit():#如果一条规则出现多个结论，则不通过，如果结论满足格式则执行如下代码
                    conclusion_list.append(backup_list[0])
                else:
                    print('一条规则仅允许有一条结论,请不要输入无关字符')
                    format_FLAG = 0  # 格式不通过
                    time.sleep(1.5)
                    break
            else:
                print('一条规则仅允许有两个元素!')
                format_FLAG=0#格式不通过
                time.sleep(1.5)
                break
            premises_list=backup_list[1].split(' ')
            for ch in premises_list:
                if ((ch.isdigit())==False) and ((ch!='')==False):
                    print('前提条件与前提条件之间用空格' '隔开,请不要输入其他字符')
                    format_FLAG = 0  # 格式不通过
                    time.sleep(1.5)
                    break
            if format_FLAG == 0:  # 格式验证未通过，要求重新输入
                continue
            Existence_FLAG=Atomic_proposition_Existence(conclusion_list,premises_list)#验证结论和前提条件原子命题存在性
            try:
                if Existence_FLAG[0]==0:
                    print(Existence_FLAG[1],'这些结论或前提条件的原子命题代号不存在，请先添加原子命题代号')
                    answer=input('是否放弃此条规则而进行下一条?(Y:放弃 N:终止规则添加)\n')
                    if answer=='Y' or answer=='y':
                        continue
                    else:
                        return
                elif Existence_FLAG[0]==1:#原子命题存在性通过则进行下一步
                    rule_existence=rules_Existence(conclusion_list,premises_list)#验证该规则存在性
                    if rule_existence==1:
                        print('此条规则已存在于规则库，将为您进行下一条规则操作')
                        time.sleep(1.5)
                        continue
                    choice=input("是否将此条规则(结论:["+",".join(conclusion_list)+"] 前提条件:["+",".join(premises_list)+"])加入规则库?(Y/N)\n")
                    if choice=='Y' or choice=='y':
                        max_num=str(int(getRule_num())+1)
                        SQL_Sentence=Rule_add_statement_selection(conclusion_list, premises_list, max_num)
                        if SQL_Sentence=="None":
                            print("添加错误")
                            print("最多支持含有八个前提条件的规则添加")
                            print('取消添加此条规则,将进行下一条规则操作')
                            time.sleep(1.5)
                            continue
                        cursor = connetion.cursor()
                        cursor.execute(SQL_Sentence)#加入规则库
                        try:
                            connetion.commit()  #提交事务,将添加的规则实时加入到数据库中
                        except Exception:
                            connetion.rollback()
                        Match(2,max_num,len(premises_list))#根据前提条件长度加入规则匹配库
                    else:
                        print('取消添加此条规则,进行下一条规则操作')
                        time.sleep(1.5)
                        continue
            except:
                print('未通过存在性验证,返回主菜单')
                time.sleep(1.5)
                return

        if format_FLAG==0:#格式验证未通过，要求重新输入
            continue
    connetion.close()


def add_Atomic_proposition_code():#添加原子命题代号
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')
    while 1:
        show_Atomic_proposition_code(1)  #通过add_Atomic_proposition_code()启用则为模式2
        print('以上为数据库已存在原子命题代号及其含义')
        print('----------添加的原子命题代号及其含义----------')
        print('PS.')
        print("1.原子命题表代号为自然数，请勿输入小数，负数等")
        print("2.含义尽量用单个英文单词表达，若有多个英文单词请用下划线'_'连接")
        print("3.原子命题表代号与含义之间用逗号,隔开")
        print("例如:  77,can't_swim    ")
        print('请输入要添加的原子命题代号及其含义,退出原子命题添加请输入quit或exit')
        cursor = connetion.cursor()
        cursor.execute("select Atomic_proposition_num from atomic_proposition;")  # 得到库中所有已存在的原子命题代号
        result_tuple = cursor.fetchall()
        designation = []
        for i in result_tuple:
            for j in i:
                num = j
                designation.append(num)
        cursor.close()  # 关闭游标，但不关闭连接，因为接下来还会用到连接
        Atomic_list=input()
        if Atomic_list.lower()=='quit' or Atomic_list.lower()=='exit':
            connetion.close()
            return
        Atomic_list=list(Atomic_list.split(','))
        if len(Atomic_list)==2:
            if Atomic_list[0].isdigit()==False:
                print("原子命题表代号为自然数")
                time.sleep(1.5)
                continue
            if Atomic_list[0] in designation:
                print("该原子命题表代号已存在,请根据原子命题代号表选择新的原子命题代号")
                time.sleep(1.5)
                continue
            ch_FLAG=1#默认字符格式通过

            for ch in Atomic_list[1]:#对含义中的每个字符遍历，出现了“_“，”,“和字母外的其他符号则返回重写
                if ((ch.isalpha()) or (ch=="'") or (ch=="_"))==False:
                    ch_FLAG=0#未通过
            if ch_FLAG==0:
                print("含义仅允许出现英文字母，下划线'_'和撇号 ' ")
                time.sleep(1.5)
                continue
        else:
            print('仅允许有两个元素，中间用逗号隔开')
            time.sleep(1.5)
            continue
        while 1:
            answer=input('请确认是否添加(Y/N)\n')
            try:
                if answer=='Y' or answer== 'y':
                    cursor = connetion.cursor()
                    meaning=Security(Atomic_list[1])
                    print(Atomic_list[0],meaning)
                    cursor.execute("insert into atomic_proposition values("+Atomic_list[0]+','+'"'+meaning+'"'+");")
                    try:
                        connetion.commit()#提交事务,将添加的原子命题代号及其含义实时加入到数据库中
                    except Exception:
                        connetion.rollback()
                    break
                elif answer=='N' or answer=='n':
                    print('放弃添加成功')
                    time.sleep(3)
                    break
            except:
                print('本次添加失败，请不要敏感词汇输入')
                time.sleep(1.5)
                break
        continue_FLAG=0#默认不再继续添加
        while True:
            choice=input('是否继续添加原子命题代号及其含义(Y/N)\n')
            if choice=='Y' or choice=='y':
                continue_FLAG=1#改为继续添加
                break
            elif choice=='N' or choice=='n':
                continue_FLAG=0
                break
            else:
                print('请不要乱输入')
                continue
        if continue_FLAG==0:
            break
        else:
            continue
    connetion.close()#关闭连接减少内存占用
    return


def rules_Existence(conclusion_list,premises_list):#规则存在性验证
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')  # 本地连接数据库
    cursor = connetion.cursor()
    cursor.execute("select premise1,premise2,premise3,premise4,premise5,premise6,premise7,premise8 from rule where conclusion="+conclusion_list[0]+";")
    result_tuple=cursor.fetchall()
    cursor.close()#关闭游标以免干扰下次查询
    rule_existence_FLAG = 0  # 默认此规则在规则库中不存在,即该规则不重复
    for i in range(len(result_tuple)):#因为一个结论可能查出多条规则，需要对每条查出来的规则都进行判断
        DB_premises_list = []
        for j in result_tuple[i]:
            if j is not None:#为了规则库后续的升级，故额外预备了列，多余的列存放NULL，通过Python得到时为None。此处去除None
                DB_premises_list.append(j)
        if len(premises_list)==len(DB_premises_list):
            count=0
            for element in premises_list:
                if element in DB_premises_list:
                    count+=1
            if count ==len(DB_premises_list):
                rule_existence_FLAG=1#说明此规则在规则库中存在,即该规则重复
    return rule_existence_FLAG


def Atomic_proposition_Existence(conclusion_list,premises_list):#原子命题代号存在性验证
    Existence_FLAG = 1 #默认原子命题代号存在
    nonexist_list=[]
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='atomic_proposition')
    for conclusion in conclusion_list:
        cursor = connetion.cursor()
        cursor.execute("select count(*) from atomic_proposition where Atomic_proposition_num="+conclusion+";")
        result1 = cursor.fetchall()
        cursor.close()
        if result1[0]==(0,):#返回结果为(0,)则说明原子命题代号不存在
            Existence_FLAG = 0
            nonexist_list.append(conclusion)
    for premise in premises_list:
        cursor = connetion.cursor()
        cursor.execute("select count(*) from atomic_proposition where Atomic_proposition_num="+premise+";")
        result2 = cursor.fetchall()
        cursor.close()
        if result2[0]==(0,):#返回结果为(0,)则说明原子命题代号不存在
            Existence_FLAG = 0
            nonexist_list.append(premise)
    return Existence_FLAG,nonexist_list


def getRule_num():#得到规则库最大序号
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule')
    cursor = connetion.cursor()
    cursor.execute("select rule_num from rule;")  # 查询结果以元组形式返回
    result = cursor.fetchall()
    cursor.close()  #关闭游标以免干扰下次查询
    num_list = []
    for i in result:
        for j in i:
            num_list.append(int(j))
    max_num=max(num_list)#max()会自动将字符串型数字转换为int型再比较大小，比较完后再转回str型,但仅限于十以内的比较，因为max仅会识别第一个字符.如'11'会被识别成1
    connetion.close()
    return  max_num


def Rule_add_statement_selection(conclusion_list,premises_list,max_num):#添加规则时的数据库语句选择,最多支持含有八个前提条件的规则添加
    if len(premises_list)==1:
        SQL_Sentence="insert into rule values("+max_num+','+conclusion_list[0]+","+premises_list[0]+",NULL,NULL,NULL,NULL,NULL,NULL,NULL);"
    elif len(premises_list)==2:
        SQL_Sentence="insert into rule values("+max_num+','+conclusion_list[0]+","+premises_list[0]+","+premises_list[1]+",NULL,NULL,NULL,NULL,NULL,NULL);"
    elif len(premises_list)==3:
        SQL_Sentence="insert into rule values("+max_num+','+conclusion_list[0]+","+premises_list[0]+","+premises_list[1]+","+premises_list[2]+",NULL,NULL,NULL,NULL,NULL);"
    elif len(premises_list)==4:
        SQL_Sentence="insert into rule values("+max_num +','+conclusion_list[0]+","+premises_list[0]+","+premises_list[1]+","+premises_list[2]+","+premises_list[3]+","+"NULL,NULL,NULL,NULL);"
    elif len(premises_list)==5:
        SQL_Sentence="insert into rule values(" + max_num + ',' + conclusion_list[0] + "," + premises_list[0] + "," +premises_list[1] + "," + premises_list[2] + "," + premises_list[3] + "," + premises_list[4] + "," + "NULL,NULL,NULL);"
    elif len(premises_list)==6:
        SQL_Sentence="insert into rule values(" + max_num + ',' + conclusion_list[0] + "," + premises_list[0] + "," +premises_list[1] + "," + premises_list[2] + "," + premises_list[3] + "," + premises_list[4] + "," + premises_list[5] + "," + "NULL,NULL);"
    elif len(premises_list)==7:
        SQL_Sentence="insert into rule values(" + max_num + ',' + conclusion_list[0] + "," + premises_list[0] + "," +premises_list[1] + "," + premises_list[2] + "," + premises_list[3] + "," + premises_list[4] + "," + premises_list[5] + "," + premises_list[6] + ",NULL);"
    elif len(premises_list)==8:
        SQL_Sentence ="insert into rule values(" + max_num + ',' + conclusion_list[0] + "," + premises_list[0] + "," +premises_list[1] + "," + premises_list[2] + "," + premises_list[3] + "," + premises_list[4] + "," + premises_list[5] + "," + premises_list[6] + "," + premises_list[7] + ");"
    else:
        SQL_Sentence="None"
    return SQL_Sentence


def Match(mode,rule_num='0',premise_len=0):
    connetion = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD,db='rule_match')
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    if mode==1:#模式一:即时前往匹配库读取每轮匹配要用的列表，最多可支持一个规则有八个前提条件
        cursor = connetion.cursor()
        cursor.execute("select rule_num from rule_match where match_round=1;")#取得第一轮匹配的列表
        result_tuple1 = cursor.fetchall()
        for i in result_tuple1:
            for j in i:
                list1.append(j)
        cursor.execute("select rule_num from rule_match where match_round=2;")#取得第二轮匹配的列表
        result_tuple2 = cursor.fetchall()
        for i in result_tuple2:
            for j in i:
                list2.append(j)
        cursor.execute("select rule_num from rule_match where match_round=3;")#取得第三轮匹配的列表
        result_tuple3= cursor.fetchall()
        for i in result_tuple3:
            for j in i:
                list3.append(j)
        cursor.execute("select rule_num from rule_match where match_round=4;")#取得第四轮匹配的列表
        result_tuple4 = cursor.fetchall()
        for i in result_tuple4:
            for j in i:
                list4.append(j)
        cursor.execute("select rule_num from rule_match where match_round=5;")#取得第五轮匹配的列表
        result_tuple5 = cursor.fetchall()
        for i in result_tuple5:
            for j in i:
                list5.append(j)
        cursor.execute("select rule_num from rule_match where match_round=6;")#取得第六轮匹配的列表
        result_tuple6 = cursor.fetchall()
        for i in result_tuple6:
            for j in i:
                list6.append(j)
        cursor.execute("select rule_num from rule_match where match_round=7;")#取得第七轮匹配的列表
        result_tuple7 = cursor.fetchall()
        for i in result_tuple7:
            for j in i:
                list7.append(j)
        cursor.execute("select rule_num from rule_match where match_round=8;")#取得第八轮匹配的列表
        result_tuple8 = cursor.fetchall()
        for i in result_tuple8:
            for j in i:
                list8.append(j)
        return list1,list2,list3,list4,list5,list6,list7,list8
        #最终返回了(['1', '2', '3', '5'], ['4', '7', '8', '12', '15'], ['6'], ['9', '10', '11', '14'], ['13'], [], [], [])
    elif mode==2:#模式二:根据前提条件列表长度将该规则加入匹配库
        cursor = connetion.cursor()
        cursor.execute("insert into rule_match values('"+str(premise_len)+"',"+rule_num+");")
        try:
            connetion.commit()  # 提交事务,将添加的规则实时加入到数据库中
        except Exception:
            connetion.rollback()
    connetion.close()


def Security(s):#对用户输入进行安全过滤
    str1 = re.sub('[!"#$%&()*+,-./:;<=>?@，。？★、…【】《》“”‘’！[\\]^`{|}~\\s]+', "", s)#使用正则表达式对用户输入进行特殊符号过滤,用于减少被SQL编码,SQL注释注入的可能
    pattern1 = re.compile('select', re.I)# 对select忽略大小写
    pattern2 = re.compile('union', re.I)  # 对union忽略大小写
    pattern3 = re.compile('where', re.I)  # 对where忽略大小写
    pattern4 = re.compile('groupby', re.I)  # 对group by忽略大小写,re.compile()的第一个元素不能有空格,否则无法匹配成功
    pattern5 = re.compile('orderby', re.I)  # 对order by忽略大小写,re.compile()的第一个元素不能有空格,否则无法匹配成功
    pattern6 = re.compile('limit', re.I)  # 对limit忽略大小写
    pattern7 = re.compile('update', re.I)  # 对update忽略大小写
    pattern8 = re.compile('delete', re.I)  # 对delete忽略大小写
    pattern9 = re.compile('insertinto', re.I)  # 对insert into忽略大小写
    pattern10 = re.compile('table', re.I)  # 对table忽略大小写
    pattern11 = re.compile('schema', re.I)  # 对schema忽略大小写
    str3=str1
    while 1:#使用re库对用户输入进行循环敏感词过滤,减少被SQL大小写和叠词绕过的可能
        str2 = str3#下一次赋值给上一次
        str3 = pattern1.sub('',str3)
        str3 = pattern2.sub('', str3)
        str3 = pattern3.sub('', str3)
        str3 = pattern4.sub('', str3)
        str3 = pattern5.sub('', str3)
        str3 = pattern6.sub('', str3)
        str3 = pattern7.sub('', str3)
        str3 = pattern8.sub('', str3)
        str3 = pattern9.sub('', str3)
        str3 = pattern10.sub('', str3)
        str3 = pattern11.sub('', str3)
        if (str2!=str3):
            continue
        else:
            break
    return str3

def main():
    DB_connection()
    while 1:
        menu()
        choice_temp = input('请选择您要进行的操作\n')
        if choice_temp in ['0', '1', '2', '3', '4','5','6','7']:
            choice = eval(choice_temp)
            if choice == 0:
                answer = input('请问您确定要退出系统吗？(y/n)\n')
                if answer == 'y' or answer == 'Y':
                    print('感谢使用')
                    break
                else:
                    continue
            elif choice==1:
                show_rules(2)
            elif choice==2:
                add_rules()
            elif choice==3:
                show_Atomic_proposition_code(2)
            elif choice==4:
                add_Atomic_proposition_code()
            elif choice==5:
                show_rule_match()
            elif choice==6:
                logical_reasoning(1)
            elif choice==7:
                fuzzy_reasoning()
            else:
                print('请别乱输!!!')
                time.sleep(1.5)
                continue



if __name__ == '__main__':#确保只有单独运行该模块时，此表达式才成立，才可以进入此判断语法，执行其中的测试代码;
    main()#如果只是作为模块导入到其他程序文件中，则此表达式将不成立，运行其它程序时，也就不会执行该判断语句中的测试代码。

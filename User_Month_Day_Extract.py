# coding:utf-8
def Extract_Date(date):
    # 
    # 01/02/2010 06:49:35
    year = date[6:10]
    day= date[3:5]
    month = date[:2]
    return year, month, day


def Extract_Month_Day(user, filePath, User_Months, User_Days):
    # user表示要分析时间的用户ID
    # filePath表示读取的数据源路径
    # User_Months表示当前该用户存在记录的月份列表
    # User_Days表示当前用户存在记录的日子列表
    Flag_Activity  = 0
    with open(filePath, 'r') as f:
        for line in f:
            line_lst = line.strip('\n').strip(',').split(',')
            # id,date,user,pc,file_tree,activity 原始格式参考
            if line_lst[2] == 'user':
                continue
            if line_lst[2] != user: # 非本用户
                continue
            if line_lst[2] == user: # 存在该用户记录
                Flag_Activity += 1 # 次数表示出现了多少次
            # date:01/02/2010 06:49:35
            year, month, day = Extract_Date(line_lst[1])
            Month_0 = year + '-' + month
            Day_0 = Month_0 + '-' + day
            if Month_0 not in User_Months:
                User_Months.append(Month_0)
            if Day_0 not in User_Days:
                User_Days.append(Day_0)
        User_Months.sort()
        User_Days.sort()
    return User_Months, User_Days, Flag_Activity


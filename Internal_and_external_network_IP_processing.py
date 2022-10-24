import re
import openpyxl
import sys
import os
import time
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Font


def getInput():
    if len(sys.argv) != 2:
        print("Usage: \n    python3  Internal_and_external_network_IP_processing.py  result.txt\n")
        exit()

    if not os.path.exists(sys.argv[1]):
        print(f"[{sys.argv[1]}] 文件不存在")
        exit()

    return sys.argv[1]


def Openfile():
    filename = getInput()
    datalist = []

    with open(filename, encoding='utf-8') as f:
        for i in f.readlines():
            datalist.append(i.strip())
    # print(datalist)

    return datalist


# 输出内网地址
def NwIp(datalist):
    sheetList = [['ip']]

    for i in datalist:
        p1 = re.findall("^(((172\.(1[6-9]|2[0-9]|3[0-1]))\..*)|^10\..*|^192\.168\..*)", i, re.S)
        # print(p1)
        ip_list = []
        if len(p1) != 0:
            p2 = list(p1)
            ip = p2[0][0]
            ip_list.append(ip)
            sheetList.append(ip_list)
            # print(ip_list)

    OutPut('内网IP', sheetList)


# 输出互联网IP地址
def WwIp(datalist):
    sheetList = [['ip']]
    ip_list = []
    for i in datalist:
        p1 = re.findall("^(((172\.(1[6-9]|2[0-9]|3[0-1]))\..*)|^10\..*|^192\.168\..*)", i)
        if len(p1) != 0:
            p2 = list(p1)
            ip = p2[0][0]
            ip_list.append(ip)
    newip = list(set(datalist) - set(ip_list))

    for l in newip:
        # print(l)
        newip_list = []
        newip_list.append(l)
        # print(newip_list)
        sheetList.append(newip_list)

    OutPut('互联网IP', sheetList)


# 表格输出整理
def OutPut(sheetname, sheetList):
    sheetName = wb.create_sheet(sheetname)

    # 将列表写入sheet
    for i in sheetList:
        sheetName.append(i)

    # 首行格式
    for row in sheetName[f"A1:{chr(65 + len(list1[0]) - 1)}1"]:
        for cell in row:
            cell.font = Font(size=12, bold=True)


if __name__ == "__main__":
    list1 = Openfile()
    wb = openpyxl.Workbook()
    NwIp(list1)
    WwIp(list1)
    ws5 = wb["Sheet"]
    wb.remove(ws5)
    input_filename = sys.argv[1].split(".txt")[0]
    Output_xlsx = (f"%s_{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.xlsx" % input_filename)
    wb.save(Output_xlsx)
    print("【🐂】处理成功！")

# -*- coding: utf-8 -*-
"""
Created on Fri May 01 10:10:31 2015

@author: Administrator
"""
import numpy as np
import scipy as sp
import pylab as pl
import h5py
import re
import os
import pandas as pd
"""
MCCB
"""
re_Find_EZD = re.compile(r"([ ][E][Z][D][\w]{4,})[ ]+([\d]{2,})")
re_Find_LV = re.compile(r"([ ][L][V][\w]{4,})[ ]+([\d]{2,})")
re_Find_Fivenumber = re.compile(r"([ ][\d]{5})[ ]+([\d]{2,})")
"""
VSD
"""
re_Find_VSD = re.compile(u"([A-Z0-9]{8,})[ ].*[ ]([\d]{0,}[,][\d]{3}|[\d]{1,3})[ ]")
"""
MAC01
"""
re_Find_MAC01=re.compile(r"[ ]([-\w]{5,})[ ].*[ ]([\d]{1,}[.][\d]{2}[ ])")
"""
LECA
"""
re_Find_LECA=re.compile(r"[ ]([-A-Z0-9]{5,})[ ].*[ ]([\d]{0,}[,][\d]{3}|[\d]{1,3})[ ]")
"""
CS002
"""
re_Find_CS002=re.compile(r"[ ]([A-Z0-9]{5,})[ ].*[ ]((?:(?:[\d]{0,}[,][\d]{3})|[\d]{1,3})[.][\d]{2}[\s])")
"""
ACB
"""
re_Find_Fivenumber = re.compile(r"([ ][\d]{5})[ ]((?:[\d]{1,}[,][\d]{3})|[\d]{1,3})[\s]")
"""
PCP
"""
re_Find_PCP=re.compile(r"([A-Z0-9]{5,})[ ].*[ ]((?:(?:[\d]{0,}[,][\d]{3})|[\d]{1,3})[.][\d]{2}[\s])")
"""
EASYPACT
"""
re_Find_33=(r"([3][3][0-9]{3})[ ]([\d]{1,}[\s])")
re_Find_NS=(r"([N][S][0-9]{5,})[ ]([0-9]{2,})[\s]")
re_Find_MVS=(r"([ ][M][V][S][\w]{5,})[ ]([0-9]{2,})[\s]")
re_Find_PA=(r"([P][A][0-9]{5,})[ ]([0-9]{2,})[\s]")
"""
C65
"""
re_Find_C65 = re.compile(r"([A-Z0-9]{5,})[ ].*[ ]([\d]{1,}[.][\d]{1}[\s])")
"""
EDM
"""
re_Find_EDM = re.compile(r"([A-Z0-9]{5,})[ ].*[ ]([\d]{1,}[.][\d]{2}[\s])")

MCCB_Price = "E:\Dropbox\Python\PriceList\Price\MCCB.txt"
ACB_Price = "E:\Dropbox\Python\PriceList\Price\ACB.txt"
CS002_Price = "E:\Dropbox\Python\PriceList\Price\CS002.txt"
VSD_Price = "E:\Dropbox\Python\PriceList\Price\VSD.txt"
MAC01_Price = "E:\Dropbox\Python\PriceList\Price\MAC01.txt"
LECA_Price = "E:\Dropbox\Python\PriceList\Price\LECA.txt"
PCP_Price = "E:\Dropbox\Python\PriceList\Price\PCP.txt"
EASYPACT_Price = "E:\Dropbox\Python\PriceList\Price\EASYPACT.txt"
C65_Price = "E:\Dropbox\Python\PriceList\Price\C65.txt"
EDM_Price = "E:\Dropbox\Python\PriceList\Price\EDM.txt"

method = {MCCB_Price:[re_Find_EZD, re_Find_LV, re_Find_Fivenumber],\
 VSD_Price:[re_Find_VSD], MAC01_Price:[re_Find_MAC01], LECA_Price:[re_Find_LECA],\
 CS002_Price:[re_Find_CS002], ACB_Price:[re_Find_Fivenumber], PCP_Price:[re_Find_PCP],\
  EASYPACT_Price:[re_Find_33, re_Find_NS, re_Find_MVS, re_Find_PA], \
  C65_Price:[re_Find_C65], EDM_Price:[re_Find_EDM]} 

def getSeriesPrice(method, fileLocation):
    """
    从价格表中读取价格函数
    """
    os.chdir("E:\Dropbox\Python\PriceList")
    with open(fileLocation) as file:
        listrow=[]
        for line in file:
                tempPriceList=re.findall(method, line)
                if tempPriceList != []:
                    for i in tempPriceList:
                        name = i[0].strip()
                        price = i[1].strip()
                        listrow.append((name, price))
        seriesPrice = pd.Series(dict(listrow))
    return seriesPrice

def annexSeriesPrice(method):
    """
    合并价格表
    """
    finalSeries=pd.Series({})    
    for file in method.keys():
        for productline in method[file]:
            finalSeries=finalSeries.append(getSeriesPrice(productline, file))
    return finalSeries.sort_index()

def abbreviateProduct(productname):
    if re.match(r"^([X]|[Z])[B].*$", productname):
        abbreviateName="DHM"
    elif re.match(r"^[L][C][1]([D]|[F]).*$", productname):
        abbreviateName="PCPD"
    elif re.match(r"^[L][C][1][E]*$", productname):
        abbreviateName="PCPE"
    elif re.match(r"^(([A][T][V])|([V][W])).*$", productname):
        abbreviateName="ATV"
    elif re.match(r"^[A][T][S].*$", productname):
        abbreviateName="ATS"
    else:
        abbreviateName="None"
    return abbreviateName
    
def getSeriesAbbreviatie():
    pricelist= annexSeriesPrice(method).sort_index()
    tempproductline=[]
    for line in pricelist.index:
        name = line
        productline=abbreviateProduct(line)
        tempproductline.append((name,productline))
    seriesAbbreviatie = pd.Series(dict(tempproductline))
    return seriesAbbreviatie

def getDataFramePrice():
    priceFrame=pd.concat([abr, price], join='inner', axis=1)
    pass
    
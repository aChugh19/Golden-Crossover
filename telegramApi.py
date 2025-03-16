import requests

def trendStocks(lis,trend,date):
    message = ''
    message += ('*******\n'+date+'\n\n'+trend.upper()+'\n*******\n')
    message+= ("\n".join(i[1] for i in lis))
    url = 'https://api.telegram.org/bot6055719169:AAE4lYwLDpUsGyLUeUWdMDdyCCU-XhfD3Yg/sendMessage?chat_id=-944176554&text=' + message
    requests.get(url)

def trades(lis,date,up=True,down=True):
    message = ''
    message += ('*******\n'+date+'\n'+'\n*******\n')
    url = 'https://api.telegram.org/bot6055719169:AAE4lYwLDpUsGyLUeUWdMDdyCCU-XhfD3Yg/sendMessage?chat_id=-944176554&text=' + message
    requests.get(url)
    for ticker,trend,buy,target,sl in lis:
        if trend=='Up' and up:
            message = ticker+':\n\tBuy=> '+str(buy)+'\n\ttarget=> '+str(target)+'\n\tStopLoss=> '+str(sl)+'\n'
        elif trend=='Down' and down:
            message = ticker+':\n\tSell=> '+str(buy)+'\n\ttarget=> '+str(target)+'\n\tStopLoss=> '+str(sl)+'\n'
        url = 'https://api.telegram.org/bot6055719169:AAE4lYwLDpUsGyLUeUWdMDdyCCU-XhfD3Yg/sendMessage?chat_id=-944176554&text=' + message
        print(message)
        requests.get(url)


def deliveryTrades(ticker,avg,now):
    message = ticker+':\n\tAverage Delivery Perc=> '+str(avg)+'\n\tToday Delivery Perc=> '+str(now)+'\n'
    url = 'https://api.telegram.org/bot6055719169:AAE4lYwLDpUsGyLUeUWdMDdyCCU-XhfD3Yg/sendMessage?chat_id=-944176554&text=' + message
    requests.get(url)
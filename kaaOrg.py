import requests
import urllib.parse as up
import pyquery as pq

# 檢查 status_code 回傳是不是 200
def detect(response):
  if response.status_code != 200:
    print('request error !')
    return

# 會員姓名
def getName():

  name = ''

  # 有 67頁
  for i in range(67):

    # 索引值從 0 開始，需要 + 1
    i += 1

    # 使用 python 3.6 以上才有的 f string 功能
    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    detect(response)

    # response.content 將回傳轉成二進制，中文才不會是亂碼
    # response.text 中文就會變成亂碼
    # 使用 PyQuery 將傳回的內容，轉成可以操作 DOM 的文件
    d = pq.PyQuery(response.content)

    # 操作 DOM 去抓要取得的資料位置
    # elems 已經變成 lxml (C語言)
    elems = d('div.mtable span.span004 > a')

    # 看有幾筆資料
    # print(len(elems))

    # .items() 將 lxml 轉回成 PyQuery
    for elem in elems.items():
      # 可以使用 jquery 的函數 .text() 取出值
      # print(elem.text())
      name += elem.text() + '\n'
  
  # 使用 with 方式，處理完畢後會自動幫你關閉檔案
  with open('kaaOrg_name.txt', 'wb') as f:
    f.write(name.encode())

# 事務所名稱
def getOffice():

  office = ''

  for i in range(67):
    i += 1

    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    d = pq.PyQuery(response.content)
    elems = d('div.mtable tr td:nth-of-type(2)')

    for elem in elems.items():
      # print(elem.text())
      office += elem.text() + '\n'

  with open('kaaOrg_office.txt', 'wb') as f:
    f.write(office.encode())

# 連絡電話
def getTel():

  tel = ''

  for i in range(67):
    i += 1

    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    d = pq.PyQuery(response.content)
    elems = d('div.mtable tr td:nth-of-type(3)')

    for elem in elems.items():
      # print(elem.text())
      tel += elem.text() + '\n'

  with open('kaaOrg_tel.txt', 'wb') as f:
    f.write(tel.encode())

# 電子郵件
def getEmail():

  email = ''

  for i in range(67):
    i += 1

    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    d = pq.PyQuery(response.content)
    elems = d('div.mtable span.span009 > a')

    for elem in elems.items():
      # print(elem.text())
      email += elem.text() + '\n'

  with open('kaaOrg_email.txt', 'wb') as f:
    f.write(email.encode())

# 傳真
def startGetTax():
  tax = ''
  tax += getTax()
  with open('kaaOrg_tax.txt', 'wb') as f:
    f.write(tax.encode())

def getTax():

  tax = ''

  for i in range(67):
    i += 1

    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    d = pq.PyQuery(response.content)
    elems = d('div.mtable span.span004 > a')

    for elem in elems.items():
      memberID = elem.attr['href'].split('?b=')[-1]
      tax += searchTax(memberID) + '\n'
    
  return tax

def searchTax(memberID):

  response = requests.get(
    f'https://www.kaa.org.tw/account_show.php?b={memberID}'
  )

  d = pq.PyQuery(response.content)
  elems = d('div.account_table > table > tr:nth-of-type(2) td')

  for elem in elems.items():
    return elem.text()

# 地址
def startGetAddress():
  address = ''
  address += getAddress()
  with open('kaaOrg_address.txt', 'wb') as f:
    f.write(address.encode())

def getAddress():

  address = ''

  for i in range(67):
    i += 1

    response = requests.get(
      f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
    )

    d = pq.PyQuery(response.content)
    elems = d('div.mtable span.span004 > a')

    for elem in elems.items():
      # print(elem.attr['href'].split('?b=')[-1])
      memberID = elem.attr['href'].split('?b=')[-1]
      address += searchAddress(memberID) + '\n'
    
  return address

def searchAddress(memberID):

  response = requests.get(
    f'https://www.kaa.org.tw/account_show.php?b={memberID}'
  )

  d = pq.PyQuery(response.content)
  elems = d('div.account_table > table > tr:nth-of-type(3) td')

  for elem in elems.items():
    return elem.text()

if __name__ == '__main__':
  startGetAddress()
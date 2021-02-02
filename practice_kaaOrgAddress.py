import requests
import urllib.parse as up
import pyquery as pq
import chardet

def start():
  address = ''
  address += getPage()
  with open('kaaOrg_address.txt', 'wb') as f:
    f.write(address.encode())

def getPage():

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
      param = elem.attr['href'].split('?b=')[-1]
      address += getAddress(param) + '\n'
    
  return address


  # for i in range(67):
  #   i += 1

  #   response = requests.get(
  #     f'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b={i}'
  #   )

  #   if response.status_code != 200:
  #     print('request error')
  #     return
  
  # 檢測 encoding: 'utf-8'
  # print(chardet.detect(response.content))

  # with open('kaaOrg_memberDiretory.html', 'wb') as f:
  #   f.write(response.content)

    # d = pq.PyQuery(response.content)
    # elems = d('div.mtable span.span004 > a[href]')
    # print(elems)

def getAddress(param):

  response = requests.get(
    f'https://www.kaa.org.tw/account_show.php?b={param}'
  )

  # with open('kaaOrg_address.html', 'wb') as f:
  #   f.write(response.content)

  d = pq.PyQuery(response.content)
  elems = d('div.account_table > table > tr:nth-of-type(3) td')

  for elem in elems.items():
    return elem.text()
    # print(elem.text())
    # with open('kaaOrg_address.text', 'wb') as f:
    #   f.write(elem.text().encode())

if __name__ == '__main__':
  start()
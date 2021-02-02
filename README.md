# Python 爬蟲練習

將 [會員目錄](https://www.kaa.org.tw/account_list.php) 的 `會員姓名` `事務所名稱` `連絡電話` `電子郵件` `傳真` `通訊地址`

比較困難的點在於 `傳真` & `地址` 需要點 `會員姓名` 後的那頁才有資料

<br>

## 觀察 url

會發現依據分頁在變的 query 是 `b=[1|2|3|...]`

- 第一頁

  https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b=1

<br>

- 第二頁

  https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b=2

<br>

- 第三頁

  https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b=3

<br>

再來點 `會員姓名`

`?b=` 後面就是 `member id`

- https://www.kaa.org.tw/account_show.php?b=MTY5MA==
- https://www.kaa.org.tw/account_show.php?b=MTY4OQ==
- https://www.kaa.org.tw/account_show.php?b=MTY4OA==

<br>

## 爬 html 結構

- https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b=1

```python
import requests
import chardet

def getPage():

  response = requests.get(
    'https://www.kaa.org.tw/account_list.php?t=0&search_input1=&search_input2=&search_input3=&search_input4=&t1=0&b=1'
  )

  if response.status_code != 200:
    print('request error !')
    return

  print(chardet.detect(response.content))
  # print(response.content)
  with open('kaaOrg_account_list.html', 'wb') as f:
    f.write(response.content)

if __name__ == '__main__':
  getPage()
```

```bash
// print(chardet.detect(response.content))

{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
```

`chardet.detect` 在檢查回傳的內容編碼是不是一致的
因為有可能 `charset=utf-8`，但實際內容確是 `big5`

```html
<head>
  <meta content="text/html; charset=utf-8" />
</head>
```

---

<br>

會輸出 `kaaOrg_account_list.html` 將裡面內容用 [HTML Formatter](https://webformatter.com/html) 轉好後複製貼上回來

```html
<!-- HTML 結構 -->
<div class="mtable">
  <table>
    <tr>
      <th class="first">會員姓名</th>
      <th>事務所名稱</th>
      <th>連絡電話</th>
      <th>電子郵件</th>
      <th>詳細資料</th>
      <th>我要委託</th>
      <th class="last"></th>
    </tr>
    <tr>
      <td>
        <span class="span004"><a href="account_show.php?b=MTY5MA==">顏欣漢</a></span>
      </td>
      <td>顏欣漢建築師事務所</td>
      <td>07-3903139</td>
      <td>
        <span class="span009"><a href="mailto:archi730@hotmail.com">archi730@hotmail.com</a></span>
      </td>
      <td><a href="account_show.php?b=MTY5MA==" class="btn_doc_s" title="簡介">簡介</a></td>
      <td><a href="quotation_show.php?b=MTY5MA==" class="btn_doc_s" title="委託">委託</a></td>
      <td></td>
    </tr>
    <tr>
      <td>
        <span class="span004"><a href="account_show.php?b=MTY4OQ==">林明璋</a></span>
      </td>
      <td>林明璋建築師事務所</td>
      <td>07-3331014</td>
      <td>
        <span class="span009"><a href="mailto:linmcaa@gmail.com">linmcaa@gmail.com</a></span>
      </td>
      <td><a href="account_show.php?b=MTY4OQ==" class="btn_doc_s" title="簡介">簡介</a></td>
      <td><a href="quotation_show.php?b=MTY4OQ==" class="btn_doc_s" title="委託">委託</a></td>
      <td></td>
    </tr>
  </table>
</div>
```

<br>

## 會員姓名

如果要抓 `事務所名稱` `連絡電話` `電子郵件`，只需要改 `d('DOM')`
記得將 `with open('檔案名稱.txt', 'wb') as f:` 要修改

```python
import requests
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

if __name__ == '__main__':
  getName()
```

<br>

## 通訊地址

```html
<!-- HTML 結構 -->
<div class="account_table">
  <h4>顏欣漢</h4>
  <h5>顏欣漢建築師事務所</h5>
  <table>
    <tr>
      <th class="botline">電　　話：</th><td class="botline">07-3903139</td>
    </tr>
    <tr>
      <th>傳　　真：</th>
      <td></td>
    </tr>
    <tr>
      <th>通訊地址：</th>
      <td>807&nbsp;高雄市三民區禮明路58號</td>
    </tr>
    <tr>
      <th>電子郵件：</th>
      <td><a href="mailto:archi730@hotmail.com">archi730@hotmail.com</a></td>
    </tr>
    <tr>
      <th>網　　址：</th>
      <td><!--a href="http://www.kaa.org.tw" target="_blank">http://www.kaa.org.tw</a--></td>
    </tr>
    <tr>
      <th class="botline">營業項目：</th>
      <td class="botline">建築規劃設計/變更使用/室內裝修/老屋(危老)重建/不動產估價/建築金融規劃/再生能源系統規劃/法令程序諮詢</td>
    </tr>
    <tr>
      <th>服務分類：</th>
      <td>
        <table>
          <tr><td>建築規劃</td><td>建築設計</td><td>土地開發規劃</td></tr><tr><td>施工方案估價</td><td>都市設計</td><td>使用變更</td></tr><tr><td>閒置空間再利用</td><td>建物安全評估(含消防)</td><td>市場及計劃研究</td></tr><tr><td>建築物公共安全檢查</td><td>建築結構設計及補強</td><td>不動產鑑估</td></tr><tr><td>景觀設計</td><td>室內設計裝修</td><td>建築設備</td></tr><tr><td>社區營造</td><td>健康建築診斷</td>
        </table>
      </td>
    </tr>
    <tr>
      <th>簡　　介：</th>
      <td>東海大學建築系畢業/高雄市政府工務局建築管理處幫工程司(104~108)/楊昭懋建築師事務所(108~109)/高雄市政府工務局委託建造照協助審查作業顧問(109~) </td>
    </tr>
  </table>
</div>
```

<br>

```python
# 通訊地址
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
```

<br>

## 補充

[爬 Google Search - 陳時中](https://hackmd.io/10Z0PdDPRw2ICluXvA4scQ?view)

[urllib - 解析 URL & 中文編碼](https://hackmd.io/1vq5r8g5QVuWZLm7ed4MAw?view)
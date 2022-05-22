# main application

from random import Random
import requests
import time
from datetime import datetime
from server import  keep_alive


AUTHORITY = "wzavfvwgfk.execute-api.us-east-2.amazonaws.com"
ORIGIN = "https://overwatchleague.com"
API_URL = "https://owlwb.glitch.me/api/live"
LOGIN_URL = "https://api.overwatchleague.com/login"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
AC = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (X11; Linux i686; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
]


def get_owl_live_match():
    response = requests.get(API_URL)
    js_res = response.json()
    match = js_res
    if not match:
        return ("", "")

    match_id = match["id"]
    live_id = match["liveID"]
    match_status = js_res["status"]
    
    referer = "https://overwatchleague.com/en-us/match/{0}/".format(match_id)
    return (match_status, referer, match_id, live_id)


user_agent = USER_AGENTS[Random().randint(0, len(USER_AGENTS) - 1)]
post_headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-GB,en;q=0.5",
    "Referer": "https://overwatchleague.com/",
    "Origin": "https://overwatchleague.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers",
    "Accept": "application/json",
    "x-origin": "overwatchleague.com",
    "Content-Type": "application/json",
}

option_headers = {
    "Accept": "*/*",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type,x-origin",
}

# == Replace the accountId below with your appuid ==

if __name__ == "__main__":
    keep_alive()
    count = 0
    while True:
        now = datetime.now()
        try:
            match_status, referer, match_id, live_id = get_owl_live_match()
            if match_status in ["", "UPCOMING"]:
                print(
                    "-" * 10,
                    "View Time: {0}min. Now: {1}".format(
                        count, now.strftime("%H:%M:%S")
                    ),
                    "-" * 10,
                )
                print("Match Not Started Yet")
                time.sleep(60)
                continue

            data = (
                '{"accountId":"123456789","type":"video_player","entryId":"bltfed4276975b6d58a", "liveTest":false,"locale":"en-us","videoId":"'
                + str(live_id)
                + '"}'
            )
            url = "https://pk0yccosw3.execute-api.us-east-2.amazonaws.com/production/v2/sentinel-tracking/owl"
            post_headers["referer"] = referer
            option_headers["referer"] = referer

            post_response = requests.post(url, headers=post_headers, data=data)
            option_response = requests.options(url, headers=option_headers)
            print(
                "-" * 10,
                "View Time: {0}min. Now: {1}".format(count, now.strftime("%H:%M:%S")),
                "-" * 10,
            )
            print(str(live_id) + " Post Response JSON: ", post_response.json())
            print("Option Response Code: ", option_response.status_code)
        except Exception as e:
            print("Failed request")
            print(e)
            time.sleep(60)

        count += 1
        time.sleep(60)

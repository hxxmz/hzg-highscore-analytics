import datetime
import requests
import json
from bs4 import BeautifulSoup


url = "https://hzgaming.net/high.php?scores=detective"
response = requests.get(url)
request_time = datetime.datetime.now() # .strftime("%A, %B %d, %Y %X")

with open('detective_highscores.json', 'r') as f:
    existing_json_data = json.load(f)

if response.status_code == 200:

    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    table_id = "one-column-emphasis" # target table id
    table = soup.find("table", id=table_id) # extract data from the HTML 

    if table: # table element was found 

        rows = table.find_all("tr") # extract data from the table 
        rows.pop(0) # popped useless header row
        rankings = []

        # print(f"*** Rankings as of {request_time.strftime('%Y-%m-%d %H:%M:%S')} ***") 

        for row in rows:
            cells = row.find_all("td")
            ranking = [cell.text.strip() for cell in cells] 
            rankings.append(ranking)
            # print(" - ".join(ranking))

    else: # table element not found
        print(f"Table with ID '{table_id}' not found.")

else:
    print(f"Request failed with status code: {response.status_code}")

new_data = [
    {
        "timestamp": request_time.isoformat(),
        "values": rankings,
        "month": request_time.month,
        "year": request_time.year,
        "day": request_time.day,
        "hour": request_time.hour
    }
]

existing_json_data["data"].append(new_data)

# with open('detective_highscores.json', 'w') as f:
#     json.dump(existing_json_data, f, indent=4) 

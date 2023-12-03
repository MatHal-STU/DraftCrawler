import re
import csv
from bs4 import BeautifulSoup

# draft_team = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', soup).group(2).strip()
# name = re.search('<h1> <span>(.*?)<\/span> <\/h1>', soup).group(1).strip()
# draft_round = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(3).strip()
# draft_overall = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(4).strip()
# draft_year = re.search('<a href="\/draft\/NHL_(\d{4})_entry.html">(.*?)<\/a>', soup).group(1).strip() 
#  re.search('<p><strong>Team Names:<\/strong>(.*?)<\/p>', html):
i= 0

with open('html_final.txt', 'r', encoding='utf-8') as file:
    a=file.read()
    pages = a.split("</html>")
f = open('output.csv', 'a', encoding='utf-8', newline="")
out = csv.writer(f, delimiter=",")
for page in pages:
    i += 1
    print(i)
    if not re.search('<h1> <span>(.*?)<\/span> <\/h1>', page):
        continue
    name = re.search('<h1> <span>(.*?)<\/span> <\/h1>', page).group(1).strip()
    name = name.encode('latin1').decode('unicode-escape').encode('latin1').decode('utf8')
    draft_team = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', page).group(2).strip()
    draft_round = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (\d+).*? round \((.*?) overall\),', page).group(3).strip()
    draft_overall = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (\d+).*? round \((\d+).*? overall\),', page).group(4).strip()
    draft_year = re.search('<a href="\/draft\/NHL_(\d{4})_entry.html">(.*?)<\/a>', page).group(1).strip() 
    position = re.search('<strong>Position<\/strong>: (.*?) (.*?);', page).group(1).strip() 
    if not re.search('<span class="(.*?)" style="">(.*?)<\/span>', page):
        nationality = 'Unknown'
    else:
        nationality = re.search('<span class="(.*?)" style="">(.*?)<\/span>', page).group(2).strip().capitalize() 
    out.writerow([name, draft_team, draft_round, draft_overall, draft_year, position,nationality])

f.close()



print(f"Occurrences have been saved in output.csv.")
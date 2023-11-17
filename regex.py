import re
import csv

# draft_team = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', soup).group(2).strip()
# name = re.search('<h1> <span>(.*?)<\/span> <\/h1>', soup).group(1).strip()
# draft_round = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(3).strip()
# draft_overall = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(4).strip()
# draft_year = re.search('<a href="\/draft\/NHL_(\d{4})_entry.html">(.*?)<\/a>', soup).group(1).strip() 
#  re.search('<p><strong>Team Names:<\/strong>(.*?)<\/p>', html):


with open('html_pokus3.txt', 'r') as file:
    text_content = file.read()

draft_team = re.findall('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', text_content)
name = re.findall('<h1>
		<span>(.*?)<\/span>
			<\/h1> ', text_content)
draft_pick = re.findall('<p><strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\), <a href="\/draft\/NHL_(\d{4})_entry.html">(.*?)<\/a> <\/p>', text_content)


print(len(draft_team))
print(len(name))
print(len(draft_pick))


csv_file_name = 'output.csv'

f = open('output.csv', 'w')
out = csv.writer(f, delimiter=",")
out.writerow([u"value1", u"value2", u"value3"])
# for match in matches:
#    out.writerow([match[1]])
f.close()

    # Write the header if needed
    # csv_writer.writerow(['Column1', 'Column2', ...])
 


print(f"Occurrences have been saved in {csv_file_name}.")
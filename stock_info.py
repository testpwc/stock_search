import requests
from BeautifulSoup import BeautifulSoup


def get_info(sym):
	payload = "http://quotes.wsj.com/{}/company-people".format(sym)
	r = requests.get(payload)
	soup = BeautifulSoup(r.text)
	stats = soup.find('table', {'class':'cr_dataTable cr_mod_average'})
	td = stats.findAll('td')
	data = {}
	for x in td:
		d =  [i.text for i in x.findAll('span')]
		data.update({d[0]:d[1]})

		

	description =  soup.find('div', {'class':"cr_description_full cr_expand"}).text
	data.update({'description':description})
	return data



for k, v in get_info('axp').items():
	if not k == "description":
		print k, v
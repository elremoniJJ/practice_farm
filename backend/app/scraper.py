from requests_html import HTMLSession


class Scraper():

    def scrapedata(self, tag):
        url = f"https://quotes.toscrape.com/tag/{tag}"
        s = HTMLSession()
        r = s.get(url)

        qlist = []

        quotes = r.html.find('div.quote')

        for q in quotes:
            item = {
                'text': q.find('span.text', first=True).text.strip(),
                'author': q.find('small.author', first=True).text.strip()
            }
            qlist.append(item)

        return qlist

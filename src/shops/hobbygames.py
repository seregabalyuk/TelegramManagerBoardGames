from requests_html import HTMLSession
from bs4 import BeautifulSoup

def url(number_page:int = 1):
  return f"https://hobbygames.ru/nastolnie?page={number_page}"

def load_html(number_page:int = 1):
  session = HTMLSession()
  html = session.get(url(number_page)).html.html
  return html

def work_with_tags(card):
  tags = card.find_all("div", class_="product-tag")
  texts = []
  for tag in tags:
    if len(tag["class"]) == 1:
      texts.append(tag.find("div", class_="product-tag__label").get_text())
  if len(texts) < 1:
    return ['0', '0'], ['0', '0'], 0
  dop = texts[0].split()
  if dop[0] == "Дополнение":
    texts.pop(0)
  if len(texts) < 3:
    return ['0', '0'], ['0', '0'], 0
  
  num_players = texts[0].split()[0].split('-')
  if len(num_players) == 1:
    num_players[0] = num_players[0].split('+')[0]
    num_players.append(num_players[0])
  
  time = texts[1].split()[0].split('-')
  if len(time) == 1:
    time = time[0].split('+')
    if len(time) == 1:
      time.append(time[0])
    else:
      time[1] = '1000'
    
  age = texts[2].split()[0].split('+')
  age.pop(-1)
  return num_players, time, age

def game_url(card):
  href = card.find("div", class_="product-card__preview").find("a")["href"]
  return f"https://hobbygames.ru{href}"

def image_url(card):
  prev = card.find("div", class_="product-card__preview")
  trig = prev.find("div", class_="product-card__trigger")
  return trig.find("img")["src"]

def parse_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  games = []
  for card in soup.find_all("div", class_="product-card__inner"):
    name = card.find("div", class_="product-card-title").find("a")["title"]
    if (name == 'Набор игр '):
      continue
    p, t, a = work_with_tags(card)
    if p == ['0', '0']:
      continue
    url = game_url(card)
    img_url = image_url(card)
    games.append((name, p, t, a, url, img_url))
  return games

def load(page_from:int = 1, page_to:int = 5):
  games = []
  for num in range(page_from, page_to + 1):
    print(f"open page {num}")
    html = load_html(num)
    print(f"close page {num}")
    games += parse_html(html)
    print(f"add games from page {num}")
  return games
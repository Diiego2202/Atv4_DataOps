from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "lunar-temple-382122",
  "private_key_id": "8f4ccc9963ecf92a93f713ba9acf96daaa6c4644",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3egdErYIa0PmJ\nZZ6TeMajn4/6xeq/0sgfdN6xXhVqnR3r4eE+yK5tJLg79m1augdWi5sfutyv/yHD\n5ulF7IaN6xSh2AC3jiYWUv1TV8t9+SOxoap9Ro+U7AaSE4dNgAHrHmAFlzAM0x7C\noyQQX55N+CBaleaLo82vZrWBGbGbN1KZ9/WijzbeJe3792Csn8z/NHu/TETQ0lsc\nX0/ab/JjYctY8m3ria2PNMi7Zcj6A5W6WuODG6+Nv1WJBTI+PPIEzBtH/Lkgg8pb\nA9Wt0/+TgoAJAcZF4w1RkCjLlxO7V8cFM0dbh7ufx+RJTicMVfbq8DlT24/tfLdB\nmdhM3j03AgMBAAECggEAFKmQ7PqPRt7W41LG33u//whGqiqky7J8qBI8zAO47LdB\n+eEHwU7PWepDNzmCyi9eCTCSqSmdldJpJos4JRBEfPIG8k0Fk6ZWAriY38xo1ch7\nbRM0RIRwQgismsHJQICUdrqGfMqwdhlGgwvlUVS7WrOBTUJJYttxG/o4oY/XsQ+C\nb9CHAz5uLFM+2glvZK2yiLm/j/WzvnI28Cd2ews/ZNDtQv2MS7r3c4fVPY81Ff1X\nalJEar8RfljJk6GVvGR7hp3ITXjxW5el+DaA2tSSyrcvMlG7GTfs1iNOUzoQj4xS\nw67FFFWX80cMxxUUUXNCTl1KEd5lH2abjb/tESJtaQKBgQDqF6VI5Jij/8Hk0UrZ\nMhbk/EiusOsTIUgPNX6Snynmh8Dwz2nS7RUSjsl6jFhrwdTddHEEG4aDGOiSkYlO\n5sWNNhMrypFovSik40CHEbX84YmYUwdu8EeqVAdj9VoDKnWXQQbrOW0X9tikZxKi\ndluiPxqUskkyQdc4/cGSWE0aTwKBgQDIpb0Ufuxg/6y/tZTXUmZi6BTpSIn13VPB\nvBidGEAMPLzt5RgKGdS7PgvbhAABRwNmelXKNgRVfi1SucWeJNWn4wU2e7p5LXic\nJpk/eaRPet/Y+Bv42fw6Y2J+gocXjR/HMBSJ8yaLR7WvrA7UFcsHCijou0rpvVh9\n7FC+fLE8mQKBgBNSCkk+3L5EYJtjDrtoX+1cSR9p6Kz2hT0EHEM7sbieIbV+WOyY\ntrGGaWic5rtWDxyL/LvrDaoKRz+5lUyWzV0/RkvJ90BexFj/jJbZRlztvG5/A9EL\nMc8ECmwcluZF/diS/GAzqCZfMDg5bZdND3kPnkEBifsE5h+FChHrCcoPAoGAEVZ4\n+y9of404QSyQmvaM0FkbjXjuKuegGCqHufNhfW02KhxUsnK+9hsLbUF/upyHR7Ck\nfx+hyj1n7zEMSXkHWUV9qtKQL25lcKDJNznsn82PUDFIQX2clPMHjMT8pWVVbKHT\n9IOlPf3JTk/AzETB0W7oUAv3EjGBVwg3he5CZmkCgYA/BwUDCfhhvtKbNM0I7NkM\n1+Qgv7AdweHa1cUPVEFQMDAGPbeOwDc50S3Qlbg0UatvpTMx9SQLez8f7//YvDsA\nGwsUP8ipS3sfXKYphybS0U+GD2v9UfWxHvTkWqJ1UKArQjhwnli3+++oi1HgAuRF\nKv1K8gYtZVW1btyqXtgxMw==\n-----END PRIVATE KEY-----\n",
  "client_email": "myaccount@lunar-temple-382122.iam.gserviceaccount.com",
  "client_id": "100208573835290801722",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myaccount%40lunar-temple-382122.iam.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atv4') ### Nome do seu bucket
  blob = bucket.blob('storage_atv4.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 

import csv
import tweepy

#Credenziali Twitter API

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Metodo che scarica gli ultimi tweet di un utente
def get_tweets(username, category):

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#Numero di tweet da scaricare
	number_of_tweets = 100

	#get tweets
	tweets_for_csv = []
	for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
        #create array of tweet information: username, tweet id, date/time, text
		tweets_for_csv.append([username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])

	#Scrivo in un csv dall'array di tweets
	outfile = category+"_"+username +".csv"
	print("writing to " + outfile)
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(tweets_for_csv)


#Lo eseguiamo da pycharm e non da command line
if __name__ == '__main__':
	#Fornisco l'username e categoria
	nome_utente="realDonaldTrump"
	categoria = "politici"
	get_tweets(nome_utente, categoria)

    #metodo alternativo:
	#scorrere tra più utenti, passo più username così verranno
	#creati tanti csv quanti sono gli utenti

	#users = ['therock','realDonaldTrump']

	#for user in users:
		#get_tweets(user,categoria)
import csv
import tweepy

#Credenziali Twitter API

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Metodo che scarica gli ultimi tweet di un utente
def get_tweets(username):

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
	#Setto il nome della categoria
	nome_categoria="politici"
	outfile = nome_categoria+"_"+username +".csv"
	print("writing to " + outfile)
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(tweets_for_csv)


#Lo eseguiamo da pycharm e non da command line
if __name__ == '__main__':
	#Fornisco l'username
	nome_utente="realDonaldTrump"
	get_tweets(nome_utente)

    #get tweets per username passato a command line
	#se lo eseguo da command line va passato il nome dell'utente
	#eliminando l'if e passando il nome dell'utente possiamo eseguirlo da GUI
    #if len(sys.argv) == 2:
    	#get_tweets("therock")
    #else:
        #print("Error: enter one username")


    #metodo alternativo: scorrere tra più utenti
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)
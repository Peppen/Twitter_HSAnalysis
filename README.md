# Twitter Hate Speech Analysis

A python script that analyse tweets and their comments to understand how much user categories are affected by hate speech. With an addition of a comparison beetween Vader and Hate Sonar results.

## Getting Started
Just clone the github repository to get all the files you need to execute the code.


### Prerequisites

All you need to install is Python 3.7 (we use Anaconda3 environment but it's the same) and these libraries:
* Twarc
* csv
* re
* Pandas
* Vader
* HateSonar
* Matplotlib


## Running and tests

script.py

* In the main change "username" and "category" to obtain results for the desired user:
> username = "twitterUsername"
> category = "The social category which the user belongs to" (It will be also a folder name) 


* Uncomment the functions that you want to use, some functions are sequential:
> get_replies
> csv_cleaning
> calculate_vaderscore/calculate_hatespeech_score
> create_score_csv 
These are the functions required to obtain replies and obtain scores calculated by the tools.

After you've obtained a good number of .csv you can generate graphs by using the functions contained in make_graph.py.
Firstly execute user_average, then you can execute one of the function to generate the graph (not both together).
The output of vader_graph and sonar_graph functions will be saved in the corresponding folder of the category.



## Built With

* [Pycharm](https://www.jetbrains.com/pycharm/) - Python IDE
* [Anaconda3](https://www.anaconda.com/) - Package Management
* [Twarc](https://github.com/DocNow/twarc) - Tool to obtain replies through twitter API
* [Vader](https://github.com/cjhutto/vaderSentiment) - Tool to analyse sentiment of the comments
* [Hate Sonar)(https://github.com/Hironsan/HateSonar) - Tool to analys sentiment of the comments with a focus on hate speech


## Authors

* **Silvio Corso** - *Initial work* - [s-corso-98](https://github.com/s-corso-98)
* **Giuseppe Napoli** - *Initial work* - [Peppen](https://github.com/Peppen)
* **Carmine Tramontano** - *Initial work* - [carminet94](https://github.com/carminet94)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
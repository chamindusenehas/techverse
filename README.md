<h1>Techverse - Questioneer </h1>
this is a flask web application developed to maintain and automate quiz competition.

<h3>how it works:</h3>
this projects used Flask as back-End technology, native javascript for making dynamic front end and MongoDb as Database technology ( the reason for using mongodb cloud database is that will help me to build a virtual network on other users because in our school, there are no networing facilities and do it through an API is also need an main server. but for this event we only had two laptops. so there are no way to maintain a main server while two players on the game.)

used simple authentication method.

there are two rounds: 

in first round, players can choose a question between 4 questions. if the first player choose a question and answer it correctly he will get scored. even he answered correctly or not, the question is locked for the both.

in the second round, when only both players are in waiting area, the game will start. both have the same questions in a raw. time for a question is 30 secs. if a player buzzed, he have 10 seconds to answer. if he answered incorrectly his score is decreased. and he can't give the correct answer, the question will passed to the opponent. he have the remained time when the other player buzzed to answer.


install required dependencies:

        py -m pip install -r requirements.txt

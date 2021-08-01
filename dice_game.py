import numpy as np
import matplotlib.pyplot as plt

def run():

	nGamesPerIteration = 100
	nIterations = 500

	#stratValScore = range(10,105,1)
	stratValRoll = range(1,34) + range(35,80,5)
	stratValScore = range(10,39,2) + range(40,105,5)
	#stratValScore = [15, 20,25]
	#stratValRoll = [3, 6]
	stratVal = stratValScore + stratValRoll
	nPlayers = len(stratVal)
	nStratValScore = len(stratValScore)
	nStratValRoll = len(stratValRoll)
	stratScore = ["score"]*(nStratValScore)
	stratRoll = ["roll"]*(nStratValRoll)
	strat = stratScore + stratRoll
	print("strat:")
	print(strat)
	print("stratVal:")
	print(stratVal)
	print(len(stratVal))
	print(len(strat))

	playerWonGames = np.zeros((nPlayers,nIterations))


	for iIteration in range(nIterations):
		for iGame in range(nGamesPerIteration):
			winner = playGame(nPlayers, strat, stratVal)
			playerWonGames[winner,iIteration] += 1.0/nGamesPerIteration

	mean = np.mean(playerWonGames,axis=1)
	std = np.std(playerWonGames,axis=1)
	print("mean:")
	print(mean)
	print("std:")
	print(std)
	if False:
		plt.plot(np.arange(nPlayers)+1,mean)
		plt.fill_between(np.arange(nPlayers)+1,mean-std,y2=mean+std, alpha=0.4)
	else:
		plt.plot(stratVal[0:nStratValScore],mean[0:nStratValScore], label='score', linewidth=3)
		plt.fill_between(stratVal[0:nStratValScore],mean[0:nStratValScore]-std[0:nStratValScore],y2=mean[0:nStratValScore]+std[0:nStratValScore], alpha=0.4)
		plt.plot(stratVal[nStratValScore+1:],mean[nStratValScore+1:],label='roll', color=[1,0,0], linewidth=3)
		plt.fill_between(stratVal[nStratValScore+1:],mean[nStratValScore+1:]-std[nStratValScore+1:],
			y2=mean[nStratValScore+1:]+std[nStratValScore+1:], color=[1,0,0], alpha=0.4)
		plt.legend()
	plt.show()

def playGame(nPlayers, strat, stratVal):
	playGame = True
	playerScoreTotals = np.zeros(nPlayers)

	while playGame :
		playerScoreTotals += playRound(strat, stratVal, nPlayers)
		#print(playRound(strat, stratVal, nPlayers))
		#print(np.max(playerScoreTotals))
		if np.max(playerScoreTotals) >= 100:
			playGame = False

	winner = np.argmax(playerScoreTotals)

	return winner


def playRound(strat, stratVal, nPlayers):
	playerScore = np.zeros(nPlayers)
	for ii in range(nPlayers) :
		nRolls = 0
		score = 0
		if strat[ii] == "roll" :
			while nRolls < stratVal[ii] :
				dieValue = throwDie()
				if dieValue == 1 :
					score = 0
					break
				else:
					score += dieValue
					nRolls += 1
		elif strat[ii] == "score" :
			while score < stratVal[ii] :
				dieValue = throwDie()
				if dieValue == 1 :
					score = 0
					break
				else:
					score += dieValue
					nRolls += 1
		playerScore[ii] = score
	return playerScore

def throwDie():
	return np.random.randint(6)+1


if __name__=="__main__":
	run()


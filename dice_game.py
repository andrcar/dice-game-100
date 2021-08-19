import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# added constraint to not play beyond 100
# all players that reach 100 win

# function for strategy selection
def run_multiplayer():

	nGamesPerIteration = 3000
	nIterations = 20

	#stratValScore = range(10,105,1)
	#stratValScore = [20.02,20.03,20.04,20.05,20.06,20.07,20.08]
	
	stratValRoll = range(4,20) + range(25,60,5)
	#stratValScore = range(10,25,2) + [25,26,33,34] + range(40,105,5) +[101,102,103]
	
	#stratValScore = [15, 20,25]
	#stratValRoll = [3,4,5,6,7,8,9,10,11,14,15,17,19]

	stratValScore = [15,20,25,34,50,100]
	stratValRoll = []

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
		fancy_plot = False
		if fancy_plot:
			fig = plt.figure(1, figsize=(12, 5))
			axes = fig.subplots(1, 2)
			mpl.rcParams.update({'font.size': 18})

			axes[0].plot(stratVal[0:nStratValScore],mean[0:nStratValScore], label='score', linewidth=4)
			axes[0].fill_between(stratVal[0:nStratValScore],mean[0:nStratValScore]-std[0:nStratValScore],y2=mean[0:nStratValScore]+std[0:nStratValScore], alpha=0.4)
			axes[0].set_xlabel('Min score per round')
			axes[0].set_ylabel('Win frequency')
			axes[0].set_title('Strategy: score')

			axes[1].plot(stratVal[nStratValScore:],mean[nStratValScore:],label='roll', color=[1,0,0], linewidth=4)
			axes[1].fill_between(stratVal[nStratValScore:],mean[nStratValScore:]-std[nStratValScore:],
				y2=mean[nStratValScore:]+std[nStratValScore:], color=[1,0,0], alpha=0.4)
			axes[1].set_xlabel('Min # throws per round')
			axes[1].set_ylabel('Win frequency')
			axes[1].set_title('Strategy: roll')
		else:
			plt.plot(stratVal[0:nStratValScore],mean[0:nStratValScore], label='score', linewidth=3)
			plt.fill_between(stratVal[0:nStratValScore],mean[0:nStratValScore]-std[0:nStratValScore],y2=mean[0:nStratValScore]+std[0:nStratValScore], alpha=0.4)
			plt.plot(stratVal[nStratValScore:],mean[nStratValScore:],label='roll', color=[1,0,0], linewidth=3)
			plt.fill_between(stratVal[nStratValScore:],mean[nStratValScore:]-std[nStratValScore:],
				y2=mean[nStratValScore:]+std[nStratValScore:], color=[1,0,0], alpha=0.4)
			plt.legend()

		#plt.legend()

	plt.show()


def run_singleplayer():

	nGamesPerIteration = 20000
	nIterations = 1
	goalScore = 100
	maxRounds = 50

	#stratValScore = range(10,105,1)
	#stratValScore = [20.02,20.03,20.04,20.05,20.06,20.07,20.08]
	
	#stratValRoll = range(4,20) + range(25,60,5)
	#stratValScore = range(10,25,2) + [25,26,33,34] + range(40,105,5) +[101,102,103]
	
	#stratValScore = [15, 20,25]
	#stratValRoll = [3,4,5,6,7,8,9,10,11,14,15,17,19]

	#stratValScore = [17,20,25,34,50,100]
	stratValScore = range(1,100,1)
	stratValRoll = []

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


	playerThrows = singleplayer_nGames(strat,stratVal,nGamesPerIteration,maxRounds,goalScore,nPlayers,nIterations)

	mean = np.mean(playerThrows,axis=1)
	std = np.std(playerThrows,axis=1)
	print("mean:")
	print(mean)
	print("std:")
	print(std)


	for iPlayer in range(nPlayers) :
		playerThrowsReduced = playerThrows[iPlayer,0:-1,0].T/nGamesPerIteration
		lbl = strat[iPlayer] + " "+ str(stratVal[iPlayer])
		plot1 = plt.figure(1)
		plt.plot(playerThrowsReduced, linewidth=3,label=lbl)
		plt.xlabel("number of rounds", fontdict=None, labelpad=None, size=20)
		plt.ylabel("probability", fontdict=None, labelpad=None, size=20)
		font = {'size'   : 16}
		plt.rc('font', **font)
		plt.legend(fontsize=18)

		plot2 = plt.figure(2)
		playerThrowsReducedCumsum = np.cumsum(playerThrowsReduced, axis=None, dtype=None, out=None)
		plt.plot(playerThrowsReducedCumsum, linewidth=3,label=lbl)
		plt.xlabel("number of rounds", fontdict=None, labelpad=None, size=20)
		plt.ylabel("cumulative probability", fontdict=None, labelpad=None, size=20)
		font = {'size'   : 16}
		plt.rc('font', **font)
		plt.legend(loc=2,fontsize=18)
	

	plot3 = plt.figure(3)

	percentiles = [2,10,25,50,75,90,98]
	throwsPercentiles = percentilesOfplayerThrows(playerThrows,percentiles,nGamesPerIteration,nPlayers,nIterations,maxRounds)
	for nPercentiles in range(len(percentiles)):
		lbl = str(percentiles[nPercentiles])
		plt.plot(throwsPercentiles[:,nPercentiles,0],linewidth=3,label=lbl)
	
	plt.xlabel("strategy value", fontdict=None, labelpad=None, size=20)
	plt.ylabel("rounds to victory", fontdict=None, labelpad=None, size=20)
	font = {'size'   : 16}
	plt.rc('font', **font)
	plt.legend(loc="upper right",fontsize=18,title="percentile")
	plt.xlim(0, 100)
	plt.ylim(0, 40)
	plt.show()
	

def percentilesOfplayerThrows(playerThrows,percentiles,nGamesPerIteration,nPlayers,nIterations,maxRounds):
	nPercentiles = np.size(percentiles,axis=0)

	throwsPercentiles = np.zeros((nPlayers,nPercentiles,nIterations))+maxRounds*1.0
	for iIteration in range(nIterations):
		for iPlayer in range(nPlayers):
			for iPercentile in range(nPercentiles):
				cumulativeVictories = 0
				for iRound in range(maxRounds):
					cumulativeVictories += playerThrows[iPlayer,iRound,iIteration]
					if cumulativeVictories > nGamesPerIteration*percentiles[iPercentile]/100:
						rest = cumulativeVictories - (nGamesPerIteration*percentiles[iPercentile]/100)
						step = playerThrows[iPlayer,iRound,iIteration]
						throwsPercentiles[iPlayer,iPercentile,iIteration] = iRound + rest/step
						break
	return throwsPercentiles


def singleplayer_nGames(strat,stratVal,nGamesPerIteration,maxRounds,goalScore,nPlayers,nIterations):
	playerThrows = np.zeros((nPlayers,maxRounds,nIterations))

	for iPlayerID in range(nPlayers):
		for iGame in range(nGamesPerIteration):
			for iIteration in range(nIterations):
				nTurns = one_player_1Game(iPlayerID,strat,stratVal,maxRounds,goalScore)
				playerThrows[iPlayerID,nTurns,iIteration] += 1

	return playerThrows

def one_player_1Game(playerID,strat,stratVal,maxRounds,goalScore):
	ii = playerID
	nTurns = 0
	totalScore = 0 
	while totalScore <= goalScore and nTurns < maxRounds-1:
		nRolls = 0
		score = 0
		if strat[ii] == "roll" :
			while nRolls < stratVal[ii] and score + totalScore <= goalScore:
				dieValue = throwDie()
				if dieValue == 1 :
					score = 0
					break
				else:
					score += dieValue
					nRolls += 1
		elif strat[ii] == "score" :
			while score < stratVal[ii] and score + totalScore <= goalScore:
				dieValue = throwDie()
				if dieValue == 1 :
					score = 0
					break
				else:
					score += dieValue
					nRolls += 1
		totalScore += score
		nTurns += 1
	return nTurns

def playGame(nPlayers, strat, stratVal):
	playGame = True
	playerScoreTotals = np.zeros(nPlayers)

	while playGame :
		playerScoreTotals += playRound(strat, stratVal, nPlayers, playerScoreTotals)
		#print(playRound(strat, stratVal, nPlayers))
		#print(np.max(playerScoreTotals))
		if np.max(playerScoreTotals) >= 100:
			playGame = False

	#winner = np.argmax(playerScoreTotals)
	winner = np.greater_equal(playerScoreTotals,100)
	#print("winner:")
	#print(winner)
	return winner




def playRound(strat, stratVal, nPlayers, playerScoreTotals):
	playerScore = np.zeros(nPlayers)
	for ii in range(nPlayers) :
		nRolls = 0
		score = 0
		if strat[ii] == "roll" :
			while nRolls < stratVal[ii] and score + playerScoreTotals[ii] <= 100:
				dieValue = ()
				if dieValue == 1 :
					score = 0
					break
				else:
					score += dieValue
					nRolls += 1
		elif strat[ii] == "score" :
			while score < stratVal[ii] and score + playerScoreTotals[ii] <= 100:
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
	#run_multiplayer()
	run_singleplayer()


def vote(candidate):
    if candidate in candidates:
        votes[candidate] = votes.get(candidate, 0) + 1
        print("Voted Successfully")
        return True

    else:
        print("Voting Failed !. Please Check your candidate name")
        return False

def print_winner():
    max_vote = max(votes.values())
    winners = [candidate for candidate, vote_count in votes.items() if vote_count == max_vote]
    print("Winner is : ")
    for winner in winners:
        print(winner, '\r')


candidates = ['Rashi', 'Farzi', 'Muhsi']
votes = {}

vote('Rashi')
vote('Farzi')
vote('Frzi')
vote('Muhsi')
vote('Muhsi')
vote('Rashi')

print_winner()

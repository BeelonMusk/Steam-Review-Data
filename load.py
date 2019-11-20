import pickle

class review:
	def __init__(self, body, label, score):
		self.corpus = body
		self.label = label
		self.score = score #tuple of (good, funny)
		self.hash = hashlib.md5(bytes(body, 'utf-8')).hexdigest()
	def __str__(self):
		return (self.label + '\n' + "'good' ratings: "+self.score[0] +'\n'+"'funny' ratings: "+self.score[1] + '\n' + self.corpus + '\n'+ "md5: " + self.hash +'\n'+'#'*50)

myReviews=[]
file = open('reviews.p', 'rb')

while True:
    try:
        myReviews.append(pickle.load(file))
    except:
        break


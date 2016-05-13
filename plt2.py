import cPickle
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectPercentile, f_classif
from matplotlib import pylab
from matplotlib.font_manager import FontProperties
import time

f = open('emails_long.pkl', 'r')
emails = cPickle.load(f)
f.close()

f = open('labels_long.pkl', 'r')
labels = cPickle.load(f)
f.close()

clfNB = GaussianNB()
clfKNN = KNeighborsClassifier(n_neighbors=5)
clfSVM = SVC(kernel = 'linear')
clfRF = RandomForestClassifier()
#clf = [clfNB, clfKNN, clfRF, clfSVM]
accNB = []
accKNN = []
accSVM = []
accRF = []
#acc = [accNB, accKNN, accRF, accSVM]
trainSize = []

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(emails, labels, test_size=0.1, random_state=42)

for i in range(10):

	features_train_small = features_train[0 : 500*(i+1)-1]
	labels_train_small = labels_train[0 : 500*(i+1)-1]

	#features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(emailsSmall, labelsSmall, test_size=0.1, random_state=42)

	vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
	features_train_transformed = vectorizer.fit_transform(features_train_small)
	features_test_transformed = vectorizer.transform(features_test)

	selector = SelectPercentile(f_classif, percentile=10)
	selector.fit(features_train_transformed, labels_train_small)
	features_train_transformed = selector.transform(features_train_transformed).toarray()
	features_test_transformed  = selector.transform(features_test_transformed).toarray()

	#t0 = time.time()
	#clf.fit(features_train_transformed, labels_train)
	#print 'training time for training set size: ', 500*(i+1), round(time.time()- t0, 3), 's'
	#t0 = time.time()
	#pred = clf.predict(features_test_transformed)
	#print 'testing time: ', round(time.time()- t0, 3), 's'

	"""for i in range(4):
		classifier = clf.pop()
		a = acc.pop()
		classifier.fit(features_train_transformed, labels_train)
		pred = classifier.predict(features_test_transformed)
		a.append(accuracy_score(labels_test, pred) * 100)"""
	clfNB.fit(features_train_transformed, labels_train_small)
	pred = clfNB.predict(features_test_transformed)
	accNB.append(accuracy_score(labels_test, pred) * 100)

	clfKNN.fit(features_train_transformed, labels_train_small)
	pred = clfKNN.predict(features_test_transformed)
	accKNN.append(accuracy_score(labels_test, pred) * 100)

	clfRF.fit(features_train_transformed, labels_train_small)
	pred = clfRF.predict(features_test_transformed)
	accRF.append(accuracy_score(labels_test, pred) * 100)

	clfSVM.fit(features_train_transformed, labels_train_small)
	pred = clfSVM.predict(features_test_transformed)
	accSVM.append(accuracy_score(labels_test, pred) * 100)


	trainSize.append((i+1) * 500)

pylab.figure(1)
pylab.xlabel('Training Set Size')
pylab.ylabel('Accuracy')

names = ['Naive Bayes', 'K Nearest Neighbours', 'Random Forest', 'SVM']
acc = [accNB, accKNN, accRF, accSVM]
style = ['solid' ,'dashed', 'dashdot', 'dotted']

for i in range(4):
	pylab.plot(trainSize, acc[i:i+1].pop(), label = names[i:i+1].pop(), ls = style[i:i+1].pop(), lw = 5)

fontP = FontProperties()
fontP.set_size('small')
art = []
lgd = pylab.legend(prop=fontP, loc='upper center', bbox_to_anchor=(0.5, 1.10), fancybox=True)
art.append(lgd)
pylab.savefig("plot4_5000.png", additional_artists=art, bbox_inches="tight")
pylab.show()




	







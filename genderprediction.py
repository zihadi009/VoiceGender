# -*- coding: utf-8 -*-
"""GenderPrediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d3hTF2YC59UUpiy2Um6CifVk3_cq2v_o
"""

pip install mglearn

# Commented out IPython magic to ensure Python compatibility.
# importing necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mglearn
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

gen = pd.read_csv('/content/shuffled_gender_voice_dataset.csv')
gen_data = pd.DataFrame(gen)
gen_data.head(100)

"""1 target variable: label (male or female)

20 independent variables:
meanfreq: mean frequency of the voice audio of the person (in kHz)
sd: standard deviation of the frequency of the voice audio
median: median frequency of the voice audio (in kHz)
Q25: first quantile (in kHz)
Q75: third quantile (in kHz)
IQR: interquantile range (in kHz)
skew: Skewness refers to a distortion or asymmetry that deviates from the symmetrical bell curve, or normal distribution
kurt: Kurtosis is a statistical measure that defines how heavily the tails of a distribution differ from the tails of a normal distribution.
sp.ent: spectral entropy
sfm: spectral flatness
mode: mode frequency
centroid: frequency centroid (see specprop)
meanfun: mean fundamental frequency measured across acoustic signal
minfun: minimum fundamental frequency measured across acoustic signal
maxfun: maximum fundamental frequency measured across acoustic signal
meandom: mean of dominant frequency measured across acoustic signal
mindom: minimum of dominant frequency measured across acoustic signal
maxdom: maximum of dominant frequency measured across acoustic signal
dfrange: range of dominant frequency measured across acoustic signal
modindx: modulation index

If the skewness is between -0.5 and 0.5, the data are fairly symmetrical.
If the skewness is between -1 and – 0.5 or between 0.5 and 1, the data are moderately skewed.
If the skewness is less than -1 or greater than 1, the data are highly skewed.
"""

# Specprop: This function returns a list of statistical properties of a frequency spectrum, which ahve been defined above.
# For more info you can visit: https://rdrr.io/cran/seewave/man/specprop.html

gen_data.isnull().sum()

gen_data.describe()

# You can see for columns like Q25 and maxdom we have very large range as compared to other columns, for this we have have to standardize or
# normalize the data. You can leave them as it si also but this may bring down the predictive power of the model.

# Convert 'label' column to numerical representation using mapping
gen_data['label'] = gen_data['label'].map({'male': 1, 'female': 0})

# Now, generate the heatmap
plt.figure(figsize=(15,15))
sns.heatmap(gen_data.corr(),annot=True,cmap='viridis',linewidths=.5)

# We already understood about correlation, from here we can see that alot of columns are directly or inversely correlated with some
# other columns having correlation value as high as 0.98
# Hence we will be removinfg some columns that don't help the model in learning or generalizing over the data.

fig, ax = plt.subplots(figsize=(4,3))
sns.countplot(gen_data['label'], ax=ax)
plt.title('Male/Female Count')
plt.show()

# There is no case of imbalance class, meaning one class doesn't dominate in the dataset.

#Plot the histograms
male = gen.loc[gen['label']=='male']
female = gen.loc[gen['label']=='female']
fig, axes = plt.subplots(10, 2, figsize=(10,20))
ax = axes.ravel()
for i in range(20):
    ax[i].hist(male.iloc[:,i], bins=20, color=mglearn.cm3(0), alpha=.5)
    ax[i].hist(female.iloc[:, i], bins=20, color=mglearn.cm3(2), alpha=.5)
    ax[i].set_title(list(male)[i])
    ax[i].set_yticks(())
    ax[i].set_xlabel("Feature magnitude")
    ax[i].set_ylabel("Frequency")
    ax[i].legend(["male", "female"], loc="best")

fig.tight_layout()

# from the graph we can see which are the columns that able to define male and female separetely.

gen_new = gen_data.drop(['median', 'Q25', 'Q75', 'centroid', 'sfm', 'skew', 'minfun', 'mindom', 'maxdom', 'dfrange'], axis = 1)

gen_new.columns

y = gen_new['label']
X = gen_new.drop(['label'], axis = 1)

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

#Train support vector machine model
svm = SVC().fit(Xtrain, ytrain)
print("Support Vector Machine")
print("Accuracy on training set: {:.2f}".format(svm.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(svm.score(Xtest, ytest)))

#Train random forest model
forest = RandomForestClassifier(n_estimators=500, random_state=42).fit(Xtrain, ytrain)
print("Random Forests")
print("Accuracy on training set: {:.2f}".format(forest.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(forest.score(Xtest, ytest)))

#Train logistic Regression model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(max_iter=1000)
logreg.fit(Xtrain, ytrain)
print("Logistic Regression")
print("Accuracy on training set: {:.2f}".format(logreg.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(logreg.score(Xtest, ytest)))

#Train Gradient Boosting Classifier model
from sklearn.ensemble import GradientBoostingClassifier
gb_clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
gb_clf.fit(Xtrain, ytrain)
print("Gradient Boosting Classifier")
print("Accuracy on training set: {:.2f}".format(gb_clf.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(gb_clf.score(Xtest, ytest)))

#Train K-Nearest Neighbour (KNN) model
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5)  # You can adjust the number of neighbors (n_neighbors)
knn.fit(Xtrain, ytrain)
print("K-Nearest Neighbors")
print("Accuracy on training set: {:.2f}".format(knn.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(knn.score(Xtest, ytest)))

#Train Decision Tree Classifier model
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(random_state=42)
tree.fit(Xtrain, ytrain)
print("Decision Tree Classifier")
print("Accuracy on training set: {:.2f}".format(tree.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(tree.score(Xtest, ytest)))

#Train Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb_classifier = GaussianNB()
nb_classifier.fit(Xtrain, ytrain)
print("Naive Bayes Classifier")
print("Accuracy on training set: {:.2f}".format(nb_classifier.score(Xtrain, ytrain)))
print("Accuracy on test set: {:.2f}".format(nb_classifier.score(Xtest, ytest)))

# Well lets go with RandonForestClassifier

# save the model to disk
import pickle
filename = 'drive/MyDrive/DataSet/voice_model.pickle'
pickle.dump(forest, open(filename, 'wb'))

filename = 'drive/MyDrive/DataSet/voice_model.pickle'  # Corrected path
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(Xtest, ytest)

import ipywidgets as widgets
from IPython.display import display
import pickle
import pandas as pd

# Load the model
filename = 'drive/MyDrive/DataSet/voice_model.pickle'
loaded_model = pickle.load(open(filename, 'rb'))

# Feature names and their full forms (updated)
feature_info = {
    'meanfreq': 'Mean Frequency',
    'sd': 'Standard Deviation',
    'IQR': 'Interquartile Range',
    'kurt': 'Kurtosis',
    'sp.ent': 'Spectral Entropy',
    'mode': 'Mode',
    'meanfun': 'Mean Fundamental Frequency',
    'maxfun': 'Maximum Fundamental Frequency',
    'meandom': 'Mean of Dominant Frequency',
    'modindx': 'Modulation Index'
}

# Create input widgets with full forms as descriptions (updated)
input_widgets = {
    feature: widgets.FloatText(description=feature_info[feature])
    for feature in feature_info
}

# Display widgets
for widget in input_widgets.values():
    display(widget)

# Predict button and function
predict_button = widgets.Button(description="Predict")

def predict_gender(button):
    input_values = [input_widgets[feature].value for feature in feature_info]
    input_data = pd.DataFrame([input_values], columns=feature_info)
    prediction = loaded_model.predict(input_data)[0]
    if prediction == 1:
        print("Predicted Gender: Male")
    else:
        print("Predicted Gender: Female")

predict_button.on_click(predict_gender)
display(predict_button)
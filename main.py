import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.nonparametric.kde import KDEUnivariate
from statsmodels.nonparametric import smoothers_lowess
from pandas import Series, DataFrame
from patsy import dmatrices
from sklearn import datasets, svm
from KaggleAux import predict as ka

df = pd.read_csv('data/train.csv')
df = df.drop(['Ticket', 'Cabin'], axis=1)
# Remove NaN values
df = df.dropna()
# print(df)

#specifies the parameters of our graphs
fig = plt.figure(figsize=(18, 6), dpi=1600)
alpha = alpha_scatterplot = 0.2
alpha_bar_chart = 0.55

# lets us plot many different shaped graphs together
ax1 = plt.subplot2grid((2, 3), (0, 0))
# plots a bar graph of those who survived vs those who did not
df.Survived.value_counts().plot(kind='bar', alpha=alpha_bar_chart)
# this nicely sets the margins in matplotlib
ax1.set_xlim(-1, 2)
plt.grid(b=True)
#puts a title on our graph
plt.title("Distribution of Survival, (1 = Survived)")

plt.subplot2grid((2, 3), (0, 1))
plt.scatter(df.Survived, df.Age, alpha=alpha_scatterplot)
# sets the y axis label
plt.ylabel("Age")
#formats the grid line style of our graphs
plt.grid(b=True, which='major', axis='y')
plt.title("Survival by Age, (1 = Surveved)")

ax3 = plt.subplot2grid((2, 3), (0, 2))
df.Pclass.value_counts().plot(kind="barh", alpha=alpha_bar_chart)
ax3.set_ylim(-1, len(df.Pclass.value_counts()))
plt.grid(b=True)
plt.title("Class Distribution")

plt.subplot2grid((2, 3), (1, 0), colspan=2)
#plots a kernel density estimate of the subset of the 1st class passengers's age
df.Age[df.Pclass == 1].plot(kind='kde')
df.Age[df.Pclass == 2].plot(kind='kde')
df.Age[df.Pclass == 3].plot(kind='kde')
# plots an axis label
plt.xlabel("Age")
plt.grid(b=True)
plt.title("Age Distribution within classes")
# sets our legend for our graph
plt.legend(('1st Class', '2nd Class', '3rd Class'), loc='best')

ax5 = plt.subplot2grid((2, 3), (1, 2))
df.Embarked.value_counts().plot(kind='bar', alpha=alpha_bar_chart)
ax5.set_xlim(-1, len(df.Embarked.value_counts()))
plt.grid(b=True)
#specifies the parameters of our graphs
plt.title("Passengers per boarding location")

plt.savefig('./1.png')


#==============================#


plt.figure(figsize=(6, 4))
fig, ax = plt.subplots()
df.Survived.value_counts().plot(kind='barh', color="blue", alpha=.65)
ax.set_ylim(-1, len(df.Survived.value_counts()))
plt.grid(b=True)
plt.title("Survival Breakdown (1 = Survived, 0 = Died)")

plt.savefig('./2.png')


#==============================#


fig = plt.figure(figsize=(18, 6))

# create a plot of two subsets, male and female, of the survived variable.
# After we do that we call value_counts() so it can be easily plotted as a bar graph
# 'barh' is just a horizontal bar graph
df_male = df.Survived[df.Sex == 'male'].value_counts().sort_index()
df_female = df.Survived[df.Sex == 'female'].value_counts().sort_index()

ax1 = fig.add_subplot(121)
df_male.plot(kind='barh', label='Male', alpha=0.55)
df_female.plot(kind='barh', color='#FA2397', label='Female', alpha=0.55)
plt.grid(b=True)
plt.title("Who survived? with respect to Gender, (raw value counts)")
plt.legend(loc='best')
ax1.set_ylim(-1, 2)

# adjust graph to display the proportions of survival by gender
ax2 = fig.add_subplot(122)
(df_male/float(df_male.sum())).plot(kind='barh', label='Male', alpha=0.55)
(df_female/float(df_female.sum())).plot(kind='barh', color='#FA2379', label='Female', alpha=0.55)
plt.grid(b=True)
plt.title("Who Survived proportionally? with respect to Gender")
plt.legend(loc='best')
ax2.set_ylim(-1, 2)

plt.savefig('./3.png')


#==============================#


fig = plt.figure(figsize=(18, 4), dpi=1600)
alpha_level = 0.65

# building on the previous code, here we create an additional within the gender subset
# we created for the survived variable. I know, that's a lot of subsets. After we do that we call
# value_counts() so it can be easily plotted as a bar graph. This is repeated for each gender
# class pair.
ax1 = fig.add_subplot(141)
female_highclass = df.Survived[df.Sex == 'female'][df.Pclass != 3].value_counts()
female_highclass.plot(kind='bar', label='female, highclass', color='#FA2379', alpha=alpha_level)
ax1.set_xticklabels(["Survived", "Died"], rotation=0)
ax1.set_xlim(-1, len(female_highclass))
plt.grid(b=True)
plt.title("Who Survived? with respect to Gender and Class")
plt.legend(loc='best')

ax2 = fig.add_subplot(142, sharey=ax1)
female_lowclass = df.Survived[df.Sex == 'female'][df.Pclass == 3].value_counts()
female_lowclass.plot(kind='bar', label='female, lowclass', color='pink', alpha=alpha_level)
ax2.set_xticklabels(["Died", "Survived"], rotation=0)
ax2.set_xlim(-1, len(female_lowclass))
plt.grid(b=True)
plt.legend(loc='best')

ax3 = fig.add_subplot(143, sharey=ax1)
male_lowclass = df.Survived[df.Sex == 'male'][df.Pclass == 3].value_counts()
male_lowclass.plot(kind='bar', label='male, lowclass', color='lightblue', alpha=alpha_level)
ax3.set_xticklabels(["Died", "Survived"], rotation=0)
ax3.set_xlim(-1, len(male_lowclass))
plt.grid(b=True)
plt.legend(loc='best')

ax4 = fig.add_subplot(144, sharey=ax1)
male_highclass = df.Survived[df.Sex == 'male'][df.Pclass != 3].value_counts()
male_highclass.plot(kind='bar', label='Male, highclass', color='steelblue', alpha=alpha_level)
ax4.set_xticklabels(["Died", "Survived"], rotation=0)
ax4.set_xlim(-1, len(male_highclass))
plt.grid(b=True)
plt.legend(loc='best')

fig.savefig('./4.png')


#==============================#


fig = plt.figure(figsize=(18, 12), dpi=1600)
a = 0.65
# Step 1
ax1 = fig.add_subplot(341)
df.Survived.value_counts().plot(kind='bar', color='blue', alpha=a)
ax1.set_xlim(-1, len(df.Survived.value_counts()))
plt.title("Step. 1")

# Step 2
ax2 = fig.add_subplot(345)
df.Survived[df.Sex == 'male'].value_counts().plot(kind='bar', label='Male')
df.Survived[df.Sex == 'female'].value_counts().plot(kind='bar', color='#FA2379', label='Female')
ax2.set_xlim(-1, 2)
plt.title("Step. 2 \nWho Survived? with respect to Gender")
plt.legend(loc='best')

ax3 = fig.add_subplot(346)
(df.Survived[df.Sex == 'male'].value_counts()/float(df.Sex[df.Sex == 'male'].size)).plot(kind='bar', label='Male')
(df.Survived[df.Sex == 'female'].value_counts()/float(df.Sex[df.Sex == 'female'].size)).plot(kind='bar', color='#FA2379', label='Female')
ax3.set_xlim(-1, 2)
plt.title("Who Survived proportionally?")
plt.legend(loc='best')

# Step 3
ax4 = fig.add_subplot(349)
female_highclass = df.Survived[df.Sex == 'female'][df.Pclass != 3].value_counts()
female_highclass.plot(kind='bar', label='female highclass', color='#FA2379', alpha=a)
ax4.set_xticklabels(["Survived", "Died"], rotation=0)
ax4.set_xlim(-1, len(female_highclass))
plt.title("Step. 3 \nWho Survived? with respect to Gender and Class")
plt.legend(loc='best')

ax5 = fig.add_subplot(3, 4, 10, sharey=ax1)
female_lowclass = df.Survived[df.Sex == 'female'][df.Pclass == 1].value_counts()
female_lowclass.plot(kind='bar', label='female lowclass', color='pink', alpha=a)
ax5.set_xticklabels(["Died", "Survived"], rotation=0)
ax5.set_xlim(-1, len(female_lowclass))
plt.legend(loc='best')

ax6 = fig.add_subplot(3, 4, 11, sharey=ax1)
male_lowclass = df.Survived[df.Sex == 'male'][df.Pclass == 3].value_counts()
male_lowclass.plot(kind='bar', label='male lowclass', color='lightblue', alpha=a)
ax6.set_xticklabels(["Died", "Survived"], rotation=0)
ax6.set_xlim(-1, len(male_lowclass))
plt.legend(loc='best')

ax7 = fig.add_subplot(3, 4, 12, sharey=ax1)
male_highclass = df.Survived[df.Sex == 'male'][df.Pclass != 3].value_counts()
male_highclass.plot(kind='bar', label='male highclass', color='steelblue', alpha=a)
ax7.set_xticklabels(["Died", "Survived"], rotation=0)
ax7.set_xlim(-1, len(male_highclass))
plt.legend(loc='best')

plt.savefig('./5.png')


#==============================#


# model formula
# here the ~ sign is an = sign, and the features of our dataset
# are written as a formula to predict survived. The C() lets our
# regression know that those variables are categorical.
# Ref: http://patsy.readthedocs.org/en/latest/formulas.html
formula = 'Survived ~ C(Pclass) + C(Sex) + Age + SibSp + C(Embarked)'
# create a results dictionary to hold our regression results for easy analysis later
results = {}

# create a regression friendly dataframe using patsy's dmatrices function
y, x = dmatrices(formula, data=df, return_type='dataframe')

# instantiate our model
model = sm.Logit(y, x)

# fit our model to the training data
res = model.fit()

# save the result for outputing predictions later
results['Logit'] = [res, formula]
res.summary()


#==============================#


# Plot Predictions v.s. Actual
plt.figure(figsize=(18, 4), dpi=1600)
plt.subplot(121, axisbg="#DBDBDB")
# generate predictions from our fitted model
ypred = res.predict(x)
plt.plot(x.index, ypred, 'bo', x.index, y, 'mo', alpha=.25)
plt.grid(color='white', linestyle='dashed')
plt.title("Logit predictions, Blue: \nFitted/predicted values: Red")

# Residuals
ax2 = plt.subplot(122, axisbg="#DBDBDB")
plt.plot(res.resid_dev, 'r-')
plt.grid(color='white', linestyle='dashed')
ax2.set_xlim(-1, len(res.resid_dev))
plt.title("Logit Residuals")

plt.savefig('./6.png')


#==============================#


fig = plt.figure(figsize=(18, 9), dpi=1600)
a = .2

# Below are example of more advanced plotting.
# If it looks strange check out the tutorial above
fig.add_subplot(221, axisbg="#DBDBDB")
kde_res = KDEUnivariate(res.predict())
kde_res.fit()
plt.plot(kde_res.support, kde_res.density)
plt.fill_between(kde_res.support, kde_res.density, alpha=a)
plt.title("Distribution of our Predictions")

fig.add_subplot(222, axisbg="#DBDBDB")
plt.scatter(res.predict(), x['C(Sex)[T.male]'], alpha=a)
plt.grid(b=True, which='major', axis='x')
plt.xlabel("Predicted chance of survival")
plt.ylabel("Gender Bool")
plt.title("The Chance of Survival Probability by Gender (1 = Male)")

fig.add_subplot(223, axisbg="#DBDBDB")
plt.scatter(res.predict(), x['C(Pclass)[T.3]'], alpha=a)
plt.xlabel("Predicted chance of survival")
plt.ylabel("Class Bool")
plt.grid(b=True, which='major', axis='x')
plt.title("The Chance of Survival Probability by Lower Class (1 = 3rd Class)")

fig.add_subplot(224, axisbg="#DBDBDB")
plt.scatter(res.predict(), x.Age, alpha=a)
plt.grid(True, linewidth=0.15)
plt.xlabel("Predicted chance of survival")
plt.ylabel("Age")
plt.title("The Chance of Survival Probability by Age")

plt.savefig('./7.png')


#==============================#


test_data = pd.read_csv("data/test.csv")
test_data['Survived'] = 1.23

# Use your model to make prediction on our test set
compared_results = ka.predict(test_data, results, 'Logit')
compared_rseults = Series(compared_results) # convert our model to a series for easy output


# output and submit to kaggle
np.savetxt("data/output/logitregres.csv", compared_results, delimiter=',')

# Create an acceptable formula for our machine learning algorithm
formula_ml = 'Survived ~ C(Pclass) + C(Sex) + Age + SibSp + Parch + C(Embarked)'


#==============================#


plt.close('all')

# set plotting parameters
plt.figure(figsize=(8, 6))

# create a regression friendly data frame
y, x = dmatrices(formula_ml, data=df, return_type='matrix')

# select which features we would like to analyze
# try changing the selection here for different output.
# Choose : [2, 3]  - pretty sweet DBs [3, 1] --standard DBs [7, 3] --very cool DBs,
# [3, 6] --very long complex dbs, could take over an hour to calculate!
feature_1 = 2
feature_2 = 3

X = np.asarray(x)
X = X[:, [feature_1, feature_2]]

y = np.asarray(y)
# needs to be 1 dimensional so we flatten. it comes out of dmatrices with a shape.
y = y.flatten()

n_sample = len(X)

np.random.seed(0)
order = np.random.permutation(n_sample)

X = X[order]
y = y[order].astype(np.float)

# do a cross validation
nighty_percent_of_sample = int(.9 * n_sample)
X_train = X[:nighty_percent_of_sample]
y_train = y[:nighty_percent_of_sample]
X_test = X[nighty_percent_of_sample:]
y_test = y[nighty_percent_of_sample:]

# create a list of the types of kernels we will use for your analysis
types_of_kernels = ['linear', 'rbf', 'poly']

# specify our color map for plotting the results
color_map = plt.cm.RdBu_r

# fit the model

for fig_num, kernel in enumerate(types_of_kernels):
    clf = svm.SVC(kernel=kernel, gamma=3)
    clf.fit(X_train, y_train)

    plt.figure(fig_num)
    plt.scatter(X[:, 0], X[:, 1], c=y, zorder=10, cmap=color_map)

    # circle out the test data
    plt.scatter(X_test[:, 0], X_test[:, 1], s=80, facecolors='none', zorder=10)

    plt.axis('tight')
    x_min = X[:, 0].min()
    x_max = X[:, 0].max()
    y_min = X[:, 1].min()
    y_max = X[:, 1].max()

    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    # put the result into a color plot
    Z = Z.reshape(XX.shape)
    plt.pcolormesh(XX, YY, Z > 0, cmap=color_map)
    plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])

    plt.title(kernel)
    plt.savefig('./8_'+str(fig_num)+'.png')



#==============================#


# Here you can output which ever result you would like by changing the kernel and clf.predict lines
# Change kernel here to poly, rbf or linear
# adjusting the gamma level also changes the degree to which the model is fitted
clf = svm.SVC(kernel='poly', gamma=3).fit(X_train, y_train)
y, x = dmatrices(formula_ml, data=test_data, return_type='dataframe')

# Change the integer values within x.ix[:, [6, 3]].dropna() explore the relationships between other
# features. the ints are columb positions. ie. [6, 3] 6th column and the third column are evaluated.
res_svm = clf.predict(x.ix[:, [6, 3]].dropna())

res_svm = DataFrame(res_svm, columns=['Survived'])
res_svm.to_csv("data/output/svm_poly_63_g10.csv") # saves the results for you, change the name as you please. 


#==============================#


# import the machine learning library that hold the randomforest
import sklearn.ensemble as ske

# Create the random forest model and fit the model to our training set
y, x = dmatrices(formula_ml, data=df, return_type='dataframe')
# RandomForestClassifier expects a 1 dimensional NumPy array, so we convert
y = np.asarray(y).ravel()
# instantiate and fit our model
results_rf = ske.RandomForestClassifier(n_estimators=100).fit(x, y)

# Score the results
score = results_rf.score(x, y)
print("Mean accuracy of Random Forest Predictions on the data was: {0}".format(score))

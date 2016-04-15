import matplotlib.pyplot as plt
import numpy as nm
x = nm.array([[-1,-1],[-2,-1],[-3,-2],[1,1],[2,1],[3,2]])
y = nm.array([1,1,1,2,2,2])

plt.xlimit(x_min, x_max)
plt.ylimit (y_min,Y_max)
plt.xticks(())
plt.yticks(())
plt.scatter(grade_sig, bumpy_sig, color="b",label="fast")
plt.scatter(grade_bkg, bumpy_bkg, color="r", label="slow")
plt.legend()
plt.xlabel("bumpiness")
plt.ylabel("grade")
plt.show()


from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features_train , labels_train)
pred = clf.predict(features_test)
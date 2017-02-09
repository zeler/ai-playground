import sys
from classifyRF import classify
from sklearn.metrics import accuracy_score

sys.path.append("../../../common")
from class_vis import prettyPicture, output_image  # noqa
from prep_terrain_data import makeTerrainData  # noqa

features_train, labels_train, features_test, labels_test = makeTerrainData()

clf = classify(features_train, labels_train)

pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)

# draw the decision boundary with the text points overlaid
prettyPicture(clf, features_test, labels_test)

# print overall accuracy of this model
print("Accuracy: " + str(acc))

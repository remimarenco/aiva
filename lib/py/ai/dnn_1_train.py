# *_train.py is for offline training, shall not be run during deployment
import numpy as np
from ai_lib import * # preprocess helpers
from sklearn import pipeline, cross_validation, metrics
import pandas
import skflow

# reliable absolute path when this module is called elsewhere
data_path = preprocess.abspath('data/titanic.csv')
model_path = preprocess.abspath('models/titanic_dnn')

# load and clean the dataset
train = pandas.read_csv(data_path)

X, y = train[['Sex', 'Age', 'SibSp', 'Fare']], train['Survived']
# chain: fillna for 'Sex' with 'NA', the rest with 0
X = X.fillna({'Sex': 'NA'}).fillna(0)

# Label Encoder to encode string entries into integers
le_X = preprocess.MultiColumnLabelEncoder(columns = ['Sex'])
X = le_X.fit_transform(X)

# random-split into train (80%), test data (20%)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=42)

# Build 3 layer DNN with 10, 20, 10 units respecitvely.
classifier = skflow.TensorFlowDNNClassifier(
  hidden_units=[10, 20, 10],
  n_classes=2,
  steps=500,
  learning_rate=0.01
)

# Fit and save model for deployment.
classifier.fit(X_train, y_train)
score = metrics.accuracy_score(y_test, classifier.predict(X_test))
print('Accuracy: {0:f}'.format(score))

# save the model for use
classifier.save(model_path)
print('Model saved to', model_path)
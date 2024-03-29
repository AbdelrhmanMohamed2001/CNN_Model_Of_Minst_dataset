from sklearn.model_selection import KFold
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD

# load train and test dataset
def load_dataset():
	(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
	# reshape dataset to have a single channel
	X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
	X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))
	# one hot encode target values
	Y_train = to_categorical(Y_train)
	Y_test = to_categorical(Y_test)
	return X_train, Y_train, X_test, Y_test


def get_pixels(train, test):
	# convert from integers to floats
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	# normalize to range 0-1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	# return normalized images
	return train_norm, test_norm

# define CNN model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (10, 10) ,padding="same", activation="relu", kernel_initializer='he_uniform', input_shape=(28, 28, 1)))        # kernel_initializer---> used to initialize all the values in the Conv2D class before actually training the model.
	model.add(MaxPooling2D((3,3 )))
	model.add(Conv2D(64, (10, 10) ,padding="same", activation='relu', kernel_initializer='he_uniform'))
	model.add(Conv2D(64, (10, 10) ,padding="same", activation='relu', kernel_initializer='he_uniform'))
	model.add(MaxPooling2D((3, 3)))
	model.add(Flatten())                                                                    #Flatten---> returns a copy of the array in one dimensional rather than in 2-D or a multi-dimensional array.
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(10, activation='softmax'))                                              #Dense---> implements the operation: output = activation(dot(input, kernel) + bias) {calculate number of parameter
	# compile model
	opt = SGD(learning_rate=0.1, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])     #compile---> converts the string to Python code object
	return model

# evaluate a model using k-fold cross-validation
def evaluate_model(dataX, dataY, n_folds=2):
	scores, histories = list(), list()
	# prepare cross validation
	kfold = KFold(n_folds, shuffle=True, random_state=2)
	# enumerate splits
	for train_ix, test_ix in kfold.split(dataX):
		# define model
		model = define_model()
		# select rows for train and test
		X_train, Y_train, X_test, Y_test = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
		# fit model
		data = model.fit(X_train, Y_train, epochs=2, batch_size=64, validation_data=(X_test, Y_test))
		# evaluate model
		_, acc = model.evaluate(X_test, Y_test)
		print('> %.3f' % (acc * 100.0))
		# stores scores
		scores.append(acc)
		history.append(data)
	return scores, history



# summarize model performance
def get_Accuracy(scores):
	# print summary
	print('Accuracy:  n=%d' % (len(scores)))


def run_test():
	# load dataset
	X_train, Y_train, X_test, Y_test = load_dataset()
	# prepare pixel data
	X_train, X_test = get_pixels(X_train, X_test)
	# evaluate model
	scores, history = evaluate_model(X_train, Y_train)

run_test()

# HCI Project
# EOG based interface :

Idea of Project:
If we have an EOG signal, it is a signal of eye movements up, down, right, left, or blink and we want to use it to set up specific tasks so that The UI should enable the user to choose whether to sleep, eat, drink water, or go to the bathroom by UI Design.

Dataset
•	We have 278 files. 
•	we have 5 Classes:

o	Yukari --> Up

o	Asagi --> Down

o	Sag --> Right 

o	Sol --> Left

o	Kirp --> Blink

•	We Use 100 File After Preprocessing.

1-Data preparation and Preprocessing:
Data Preparation:
1)	The Signals is a reading manual Use ReadSignal () Function.
2)	preprocessing on this Signals.
3)	Feature Extraction Using 5 Ways.
4)	Concatenate Horizontal with Vertical Data in one Signal.
5)	The dataset is split into training and testing sets using the train_test_split function from the sklearn library.
6)	The training data is used to fit the model and the testing data is used to evaluate the model's performance.
Preprocessing:
1)	Filter Signals by reading files that contain only h and v in their name with same number of signal and neglected anything else and Single Signal.
2)	use a band pass filter With “lowCutoff=.5” & “highCutoff=20”. 
3)	Down Sampling to half Using Resample () Function.
4)	Normalization Signals Manual Using Z-Score.
5)	Remove DC Component in Signal by Subtract Signal Median.
6)	Label Encoder for Classes:
o	Yukari --> Up --> 4.
o	Asagi --> Down --> 0.
o	Sag --> Right --> 2.
o	Sol --> Left --> 3.
o	Kirp --> Blink --> 1.

2- Feature extraction methods: 
We Use 5 Ways to Feature Extraction:
- In Frequency Domain Features: 
1)	Compute Statistical features from wavelet coefficients.
2)	Power Spectral Density (PSD): signal's power content versus frequency.

- In Time Domain Features:
1)	Compute Morphological features from filtered signals:
a.	Max peak values Features: Firstly, find all peaks in each signal then find the max peak value.
b.	Area under curve Features: it’s meant the integration of the function of curve.
2)	Auto Regression Coefficients: A statistical model is autoregressive if it predicts future values based on past values.

3- Classification Models and parameters:
•	K-Nearest Neighbors (KNN):
•	The parameters used for the KNeighborsClassifier classifier are k = 5 # Number of nearest neighbors to consider.
•	Support Vector Machine Classifier (SVM):
•	The parameters used for the SVC classifier are (kernel='linear', C=1.0).
•	Random Forests:
•	The parameters used for the RF classifier are n_trees = 100 # Number of trees in the forest.

4- Classification results:
1)	KNN:
#	Feature extraction	Accuracy
1	Compute Statistical features from wavelet coefficients	45 ~ 70 %
2	Power Spectral Density (PSD)	20 ~ 35 %
3	Compute Morphological features from filtered signals Using Max peak values	75 ~ 100 %
4	Compute Morphological features from filtered signals Using Area under curve	30 ~ 65 %
5	Auto Regression Coefficients	50 ~ 75 %

2)	Support Vector Machine:
#	Feature extraction	Accuracy
1	Compute Statistical features from wavelet coefficients	50 ~ 80 %
2	Power Spectral Density (PSD)	30 ~ 55 %
3	Compute Morphological features from filtered signals Using Max peak values	70 ~ 100 %
4	Compute Morphological features from filtered signals Using Area under curve	40 ~ 70 %
5	Auto Regression Coefficients	45 ~ 80 %

3)	Random Forests:
#	Feature extraction	Accuracy
1	Compute Statistical features from wavelet coefficients 	80 ~ 100 %
2	Power Spectral Density (PSD)	20 ~ 45 %
3	Compute Morphological features from filtered signals Using Max peak values	70 ~ 100 %
4	Compute Morphological features from filtered signals Using Area under curve	30 ~ 65 %
5	Auto Regression Coefficients	80 ~ 95 %


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from scipy.signal import butter,filtfilt
from scipy import signal
import scipy.signal as s
import pywt
import scipy.integrate as integrate
from sklearn.metrics import accuracy_score
import warnings
from sklearn import neighbors
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
warnings.filterwarnings('ignore')

from statsmodels.tsa.ar_model import AutoReg
def ReadSignal(path):
    
    EOG_Signal = open(path,"r")
    lines = EOG_Signal.readlines()
    AMP=[]
    for i in range(len(lines)-1):
        L=lines[i+1]
        AMP.append(int(L))
    return AMP
def DrawSignal(signal1):
    plt.Figure(figsize=(12,6))
    plt.plot(np.arange(0,len(signal1)), signal1)
    plt.xlabel('time(s)')
    plt.ylabel('signal(v)')
    plt.show()
    # EOG_Signal = open("dataset/asagi1v.txt","r")
    
def ButterBbandpassFilter(inputSignal,lowCutoff,highCutoff,samplingRate,order):
    nyq = .5 * samplingRate
    low = lowCutoff / nyq
    high = highCutoff / nyq
    numerator , denominator = butter(order,[low,high],btype='band',output='ba',analog=False,fs=None)
    filtered = filtfilt(numerator, denominator, inputSignal)
    return filtered

def RemoveDCComponent(signal1):
    # Calculate median value signal
    signalMedian = np.median(signal1)
    
    # Subtract baseline median from signal
    eog_corrected = signal1 - signalMedian
    return eog_corrected

def Normalization(siganl):
    # Z-score normalization
    eogZscore = (siganl - np.mean(siganl)) / np.std(siganl)
    return eogZscore

def Resample(signal1,number):
    resampleSianl = s.resample(signal1, number)
    return resampleSianl

def GetFMax(signal1):
    # Calculate the Fourier transform of the signal
    fft = np.fft.fft(signal1)
    
    # Calculate the power spectral density (PSD) of the signal
    psd = np.abs(fft)**2 / len(fft)
    
    # Calculate the corresponding frequency values for each PSD value
    freqs = np.fft.fftfreq(len(signal1), 1/1000) # 1000 Hz sampling rate
    
    # Find the index of the maximum PSD value in the frequency range of interest
    freq_range = np.where((freqs >= 0.1) & (freqs <= 30))[0] # frequency range of interest
    max_psd_idx = np.argmax(psd[freq_range])
    
    # Get the corresponding frequency value for the maximum PSD value
    max_freq = freqs[freq_range][max_psd_idx]
    
    return max_freq

def PreprocessingEOGSignal(signal):
    # DrawSignal(signal)
    # print(signal,len(signal))
    filterSignal = ButterBbandpassFilter(signal, lowCutoff=.5, highCutoff=20, samplingRate=176, order=2)
    # DrawSignal(filterSignal)
    # print(filterSignal,len(filterSignal))
    filterSignal = Resample(filterSignal, len(signal) //2)
    # DrawSignal(filterSignal)
    # print(filterSignal,len(filterSignal))
    filterSignal = Normalization(filterSignal)
    # DrawSignal(filterSignal)
    # print(filterSignal,len(filterSignal))
    filterSignal = RemoveDCComponent(filterSignal)
    # DrawSignal(filterSignal)
    # print(filterSignal,len(filterSignal))
    return filterSignal

#Frequency Domain Feature

def FeatureExtracionByWavelets(signal):
    # Perform wavelet decomposition on the signal
    coeffs = pywt.wavedec(signal, 'db4')
    # Extract features from the wavelet coefficients
    coeffs_mean = []
    coeffs_std = []
    eog_features =[]
    for c in coeffs:
        coeffs_mean.append(np.mean(c))
        coeffs_std.append(np.std(c))
        # Extract wavelet coefficients as features
    return np.array(coeffs_mean + coeffs_std) 

def FeatureExtracionByPSD(signal):
    fs =2* GetFMax(signal)
    (f,psd)= s.periodogram(signal,fs,scaling='density')
    psd_mean = np.mean(psd)
    psd_std = np.std(psd)
    psd_max = np.max(psd)
    psd_min = np.min(psd)
    psd_peak_frequency = f[np.argmax(psd)]
    features = [psd_mean , psd_max, psd_std , psd_min ,psd_peak_frequency ]
    return features

#Time Domain Feature
def FeatureExtracionByPeaks(siganl):
    x=[]
    y=[]
    peaks ,_ = s.find_peaks(siganl)
    for i in range(len(peaks)-1):
        y.append(siganl[peaks[i]])
        x.append(peaks[i])
    peakMax = max(y)
    return peakMax
    
def FeatureExtracionByAutoReg(signal):
    model= AutoReg(signal, lags=4)
    model_fit= model.fit()
    return model_fit.params

def FeatureExtracionByArea(signal):
    i1 = integrate.simpson(signal)
    return i1

def FeatureExtracion(siganls, method):
    
    Feature = []
    if method == 1:
        for signal in siganls:
            Feature.append(FeatureExtracionByWavelets(signal))
    elif method == 2:
        for signal in siganls:
            Feature.append(FeatureExtracionByPSD(signal))
    if method == 3:
        for signal in siganls:
            Feature.append(FeatureExtracionByAutoReg(signal))
    if method == 4:
        for signal in siganls:
            Feature.append(FeatureExtracionByPeaks(signal))
    if method == 5:
       for signal in siganls:
           Feature.append(FeatureExtracionByArea(signal))
    return Feature
def main():
    labels_H =[]
    labels_V =[]
    signals_H = []
    signals_V =[]
    feature_H =[]
    feature_V =[]
    
    files = os.listdir("./dataset")
    # print(files)
    for file in files:
        if 'h' in file:
            v = file.replace('h', 'v')
            if v not in files:
                continue
        elif 'v' in file:
            h = file.replace('v', 'h')
            if h not in files:
                continue
        signal = ReadSignal("dataset/"+file)
        signal = PreprocessingEOGSignal(signal)
        label = -1
        if file.startswith('asagi'):    
            label = 0
            if file.endswith('v.txt'):
                signals_V.append(signal)
                labels_V.append(label)
            else:
                signals_H.append(signal)
                labels_H.append(label)
        elif file.startswith('kirp'):
            label = 1
            if file.endswith('v.txt'):
                signals_V.append(signal)
                labels_V.append(label)
            else:
                signals_H.append(signal)
                labels_H.append(label)
        elif file.startswith('sag'):
            label = 2
            if file.endswith('v.txt'):
                signals_V.append(signal)
                labels_V.append(label)
            else:
                signals_H.append(signal)
                labels_H.append(label)
        elif file.startswith('sol'):
            label = 3
            if file.endswith('v.txt'):
                signals_V.append(signal)
                labels_V.append(label)
            else:
                signals_H.append(signal)
                labels_H.append(label)
        elif file.startswith('yukari'):
            label = 4
            if file.endswith('v.txt'):
                signals_V.append(signal)
                labels_V.append(label)
            else:
                signals_H.append(signal)
                labels_H.append(label)
    # print(signals_H,len(signals_H))
    feature_H = FeatureExtracion(signals_H, 4)
    feature_V = FeatureExtracion(signals_V, 4)
    data_H =pd.DataFrame(feature_H)
    
    data_V =pd.DataFrame(feature_V)
    
    
    data = pd.concat([data_H, data_V], axis=1)
    
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels_H, test_size=0.2,)
    
    # Train an SVM classifier
    clf = SVC(kernel='linear', C=1.0)
    clf.fit(X_train, y_train)
    
    # Predict the labels for the test set
    y_pred = clf.predict(X_test)
    
    # Evaluate the accuracy of the classifier
    accuracy = accuracy_score(y_test, y_pred)
    if accuracy >= .95:
        dump(clf, f'modelSVM{accuracy*100}Area.svm')
    
    print("Accuracy SVM:", accuracy)
    
    #  Train the KNN model
    k = 5 # Number of nearest neighbors to consider
    knn_model = neighbors.KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X_train, y_train)
    
    #  Test the KNN model
    predictions = knn_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    if accuracy >= .95:
        dump(knn_model, f'modelKNN{accuracy*100}Area.knn')
    
    print("Accuracy KNN:", accuracy)
    
    
    #  Train the Random Forest model
    n_trees = 100 # Number of trees in the forest
    max_depth = None # Maximum depth of the decision trees
    random_forest_model = RandomForestClassifier(n_estimators=n_trees, max_depth=max_depth)
    random_forest_model.fit(X_train, y_train)
    
    #  Test the Random Forest model
    predictions = random_forest_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    if accuracy >= .95:
        dump(knn_model, f'modelRF{accuracy*100}Area.rf')
    
    print("Accuracy RF:", accuracy)
    
    predictions = knn_model.predict(X_test)
    print(predictions , y_test)
    
if __name__ == '__main__':
    main()
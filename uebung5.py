
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

def readSample(filename,title='',sampleSize=0):
    #dataDirectory = 'C:\\Users\\Diehl\\Desktop\\Vorlesungen\\FST\\BOA\\'
    dataDirectory = 'D:\Github\\test\\fst\\boa\\'
    # filename kann auch ein URL sein: "https://..../example.csv"
    df = pd.read_csv(dataDirectory+filename,
                     sep=r"\[|\]\s=",
                     engine="python",
                     index_col=False,
                     #nrows=25, # zum Testen nur kleine Anzahl einlesen
                     skipinitialspace=True,
                     names=['Variable', 'Project', 'Ratio'],
                     usecols=['Project', 'Ratio']
                     )
    if sampleSize>0:
        df = df.sample(sampleSize, random_state=1)
    df.info()
    df.boxplot(column=['Ratio'], grid=False)
    df.hist(column=['Ratio'], grid=False)
    plt.title(title)
    plt.show()
    return df

def main():
    plt.close('all')
    print('Statistische Berechnungen zu Häufigkeiten (Übung 5)')
    print('\nEinlesen der ersten Stichprobe (Python)')
    pythonSample=readSample('pythontryratio.boa.output.txt',
                            sampleSize=1000,
                            title="Python")
    print('Mean:' + str(pythonSample['Ratio'].mean()))
    print('Variance:'+str(pythonSample['Ratio'].var()))
    print('\nEinlesen der zweiten Stichprobe (Java)')
    javaSample = readSample('javatryratio.boa.output.txt',
                            sampleSize=1000,
                            title="Java")
    print('Mean:' + str(javaSample['Ratio'].mean()))
    print('Variance:' + str(javaSample['Ratio'].var()))

    print('\nStatistische Tests')

    ### HIER SOLLTE IHR PROGRAMMKODE FOLGEN !!!

    stat, p = stats.mannwhitneyu(javaSample['Ratio'], pythonSample['Ratio'])
    print('Mann-Whitney test: Stat: '+ str(stat) + ', p-Wert: ' + str(p))
    if p < 0.01:
        print('statistisch signifikant')
    else:
        print('nicht statistisch signifikant')

    mean_diff = pythonSample['Ratio'].mean() - javaSample['Ratio'].mean()
    pooled_std = ((pythonSample['Ratio'].std() ** 2 + javaSample['Ratio'].std() ** 2) / 2) ** 0.5
    cohens_d = mean_diff / pooled_std

    print('Cohen\'s d: ' + str(cohens_d))

    size = 1000
    while size > 0:
        pythonSampleSize = pythonSample.sample(size)
        javaSampleSize = javaSample.sample(size)
        stat, p = stats.mannwhitneyu(javaSampleSize['Ratio'], pythonSampleSize['Ratio'])
        if p >= 0.01:
            print('nicht signifikant ab Size: ' + str(size))
            break
        size -= 1
    if size == 0:
        print('Keine Schranke')

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



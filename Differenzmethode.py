datvon = "/run/media/va/VOLUME/Messungen/20160718/Au-LNMO/fit.amp"
datnach = "/run/media/va/VOLUME/Messungen/20160718/Au-LNMO/fit-sortiert.amp"


if __name__ == '__main__':
    datei = file(datvon)
    datei.readline()
    werte = datei.readline().split('\t')[1:]
    sortiert = ['']*len(werte)
    for n in range(len(werte)/2+1):
        sortiert[2*n] = werte[n] + '\n'
        try:
            sortiert[2*n+1] = werte[len(werte)/2+1+n].rstrip('\n') + '\n'
        except IndexError:
            pass
    file(datnach, 'w').writelines(sortiert)


datvon = "/home/sebadur/Dokumente/Messungen/20160906/m1.amp"
datnach = "/home/sebadur/Dokumente/Messungen/20160906/m1ac.amp"


if __name__ == '__main__':
    datei = file(datvon)
    ac = [el[el[:-5].rfind(' ')+1:-5] for el in datei.readline().replace('\n', '').split('\t')[1:]]
    messwerte = [zeile.replace('\n', '').split('\t')[1:] for zeile in datei.readlines()]
    datei = file(datnach, 'w')

    for n in range(len(ac)):
        datei.write(ac[n])
        for dc in messwerte:
            datei.write('\t' + dc[n] + '\n')

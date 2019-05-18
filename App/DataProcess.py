import csv
import jieba
class DataProcess():
    def process(self):
        f=open("data/distribute_collectt.csv","rt", encoding="utf-8")
        lines=f.readlines()
        for line in lines:
            words=jieba.cut(line)
            rows = []
            for word in words:
                if(len(word)>1):
                    rows.append(word)
            out = open('data/distribute_clean.csv', 'a', newline='', encoding="utf-8")
            csv_writer = csv.writer(out)
            csv_writer.writerow(rows)
        f.close()

if __name__ == '__main__':
    DataProcess().process()
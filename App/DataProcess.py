import csv
import jieba
class DataProcess():
    def process(self):
        f=open("data/distribute.csv","rt", encoding="utf-8")
        lines=f.readlines()
        print(lines)
        for line in lines:
            print(line)
        f.close()

if __name__ == '__main__':
    DataProcess().process()
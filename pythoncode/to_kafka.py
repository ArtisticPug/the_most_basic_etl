import io, chardet, os, codecs, re, json
from kafka import KafkaProducer
from time import sleep


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)

filename = 'skazka.txt'

bytes = min(32, os.path.getsize(filename))
raw = open(filename, 'rb').read(bytes)

if raw.startswith(codecs.BOM_UTF8):
    encoding = 'utf-8-sig'
else:
    result = chardet.detect(raw)
    encoding = result['encoding']

infile = io.open(filename, 'r', encoding=encoding)
data = infile.read()
infile.close()


list = re.findall(r'\b\w{3,}\b', data)
if __name__ == "__main__":
    for el in list:
        producer.send('test', el.lower())
        sleep(1)

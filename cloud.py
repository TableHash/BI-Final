import jieba
import re
from wordcloud import WordCloud
from zhon.hanzi import punctuation
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def jieba_cut(x, sep=' '):
    return sep.join(jieba.cut(x, cut_all=False))

file_object = open('input/data1.txt','rU')
try:
    file_context = file_object.read()
finally:
     file_object.close()

file_context=re.sub(r"[%s]+" %punctuation, "", file_context)

print('raw', file_context)
print('cut', jieba_cut(file_context, ', '))

content=jieba_cut(file_context,',')

mask=np.array(Image.open('input/dang.png'))
wc = WordCloud(font_path="input/MonacoYahei.ttf", background_color='white',mask=mask)
wc.generate(content)

plt.figure(figsize=[16, 16])
plt.imshow(wc)
plt.title('19th National Congress of the Communist Party of China')
plt.axis('off')
plt.show()
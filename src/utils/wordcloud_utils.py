import base64
import io
from wordcloud import WordCloud
from init_utils import *


root = init_by_key('root')


def dic2text(dic):
    text = ''
    s = set()
    ch_l = {'__label__ACADEMIC':'人才团队',
            '__label__PATENTS':'专利奖项',
            '__label__INVESTMENT':'投融资',
            '__label__BUSINESS':'商业市场',
            '__label__INDUSTRIAL':'产业',}
    if('FILES' in dic.keys()):
        files = dic['FILES']
        for f in files:
            labels = f['LABELS']
            etys = f['ENTITYS']
            for l in labels.keys():
                if(ch_l[l] not in text):
                    text = text + (ch_l[l]+' ')*int(labels[l]['score']*5)
                items = labels[l]['items']
                for i in items:
                    s.add(i)
                    if( i not in text):
                        text = text + (i+' ')
            for ety in etys:
                if(ety['name'] not in text):
                    s.add(ety['name'])
                    text = text + (ety['name']+' ')*int(ety['score']*2.5)
    return text,s






def word_cloud(text):
    # def get_word_cloud(text):
    # pil_img = WordCloud(width=500, height=500, font_path=font).generate(text=text).to_image()
    # color_mask = numpy.array(Image.open(root+'data/wordcloud/mask/mask.png')) # 打开背景图片
    pil_img = WordCloud(font_path=root+'data/wordcloud/fonts/simhei.ttf',
                        width=800,
                        height=300,
                        # mask=color_mask,
                        background_color="white").generate(text=text).to_image()

    # plt.imshow(pil_img)
    # plt.show()
    #
    # plt.axis("off")
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64

def json2img(dic):
    txt,s = dic2text(dic)
    img_base64 = word_cloud(txt)
    return img_base64,s

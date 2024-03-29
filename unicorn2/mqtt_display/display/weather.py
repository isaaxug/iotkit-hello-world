#!/usr/bin/env python3
# coding: utf-8

from logging import getLogger
logger = getLogger(__name__)

from .unicorn_weather_official_icon import getWeather, filterNearstWeather
from PIL import Image
import datetime
import unicornhathd
import requests
import time
import os

APIKEY = os.environ.get('OPENWEATHER_API_KEY')
CYCLE_TIME = 0.5

# Open Weather APIとPNGアニメーションのマッピング
ICON_TABLE = {
    '01d': 'clear-day.png',
    '01n': 'clear-night.png',
    '02d': 'partly-cloudy-day.png',
    '02n': 'partly-cloudy-night.png',
    '03d': 'cloudy.png',
    '03n': 'cloudy.png',
    '04d': 'cloudy.png',
    '04n': 'cloudy.png',
    '09d': 'rain.png',
    '09n': 'rain.png',
    '10d': 'rain.png',
    '10n': 'rain.png',
    '11d': 'rain.png',
    '11n': 'rain.png',
    '13d': 'snow.png',
    '13n': 'snow.png',
    '50d': 'fog.png',
    '50n': 'fog.png',
    'error': 'error.png'
}

CURRENT_DIR = os.path.dirname(__file__)
WEATHER_ICONS_DIRECTORY = os.path.join(CURRENT_DIR, 'weather-icons', 'icons')
if not os.path.exists(WEATHER_ICONS_DIRECTORY):
    raise RuntimeError('Icon directory not found. (%s)', WEATHER_ICONS_DIRECTORY)

width, height = unicornhathd.get_shape()


def drawAnimation(image, event):
    for o_x in range(int(image.size[0] / width)):
        for o_y in range(int(image.size[1] / height)):
            valid = False
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel(((o_x * width) + y, (o_y * height) + x))
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicornhathd.set_pixel(x, y, r, g, b)

            if event.is_set():
                return

            if valid:
                unicornhathd.show()
                time.sleep(CYCLE_TIME)


def main(event, city):
    """
    メイン処理
    これをループし続ける
    """

    # 現在時刻の取得
    now = datetime.datetime.now()

    # datetimeオブジェクトをUnixTimeに変換し、ターゲット時間を作る
    # ターゲットを2時間先とする
    target_timestamp = now.timestamp() + 60 * 60 * 2

    try:
        r = getWeather(city, APIKEY)
        if not r.ok:
            logger.warn('error, weather get fail')
            time.sleep(30 * 3)
            return

        weathers = r.json()['list']

        weather = filterNearstWeather(weathers, target_timestamp)

        logger.debug('{1}\'s weather is {0}'.format(weather, city))

        iconname = ICON_TABLE[weather['weather'][0]['icon']]

        image = Image.open(os.path.join(WEATHER_ICONS_DIRECTORY, iconname))

        if image is None:
            logger.warning("image is None.")
            time.sleep(30 * 3)
            return

    except requests.exceptions.ConnectionError as e:
        logger.exception(e)
        time.sleep(30 * 3)

    except KeyError:
        time.sleep(30 * 3)
        return

    logger.debug('start write icon.')

    for i in range(0, 300):
        if event.is_set():
            break

        drawAnimation(image, event)

    logger.debug('end of one cicle.')

def loop(event, city):
    unicornhathd.rotation(90)

    logger.debug('{} loop stert.'.format(city))
    while not event.is_set():
        main(event, city)

    logger.debug('{} loop end.'.format(city))

#!/usr/bin/env python3
# coding: utf-8

from logging import getLogger
from logging import Formatter, StreamHandler
import sys
logger = getLogger(__name__)
logger.setLevel('DEBUG')
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(
    Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
)
logger.addHandler(handler)

from .unicorn_weather_official_icon import getWeather, filterNearstWeather
from PIL import Image
import datetime
import unicornhathd
import requests
import time
import os

APIKEY = os.environ.get('OPENWEATHER_API_KEY')
CYCLE_TIME = 0.5

# Open Weather APIとPNGアニメーションのマッピング
ICON_TABLE = {
    '01d': 'clear-day.png',
    '01n': 'clear-night.png',
    '02d': 'partly-cloudy-day.png',
    '02n': 'partly-cloudy-night.png',
    '03d': 'cloudy.png',
    '03n': 'cloudy.png',
    '04d': 'cloudy.png',
    '04n': 'cloudy.png',
    '09d': 'rain.png',
    '09n': 'rain.png',
    '10d': 'rain.png',
    '10n': 'rain.png',
    '11d': 'rain.png',
    '11n': 'rain.png',
    '13d': 'snow.png',
    '13n': 'snow.png',
    '50d': 'fog.png',
    '50n': 'fog.png',
    'error': 'error.png'
}

CURRENT_DIR = os.path.dirname(__file__)
WEATHER_ICONS_DIRECTORY = os.path.join(CURRENT_DIR, 'weather-icons', 'icons')
if not os.path.exists(WEATHER_ICONS_DIRECTORY):
    raise RuntimeError('Icon directory not found. (%s)', WEATHER_ICONS_DIRECTORY)

width, height = unicornhathd.get_shape()


def drawAnimation(image, event):
    for o_x in range(int(image.size[0] / width)):
        for o_y in range(int(image.size[1] / height)):
            valid = False
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel(((o_x * width) + y, (o_y * height) + x))
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicornhathd.set_pixel(x, y, r, g, b)

            if event.is_set():
                return

            if valid:
                unicornhathd.show()
                time.sleep(CYCLE_TIME)


def main(event, city):
    """
    メイン処理
    これをループし続ける
    """

    # 現在時刻の取得
    now = datetime.datetime.now()

    # datetimeオブジェクトをUnixTimeに変換し、ターゲット時間を作る
    # ターゲットを2時間先とする
    target_timestamp = now.timestamp() + 60 * 60 * 2

    try:
        r = getWeather(city, APIKEY)
        if not r.ok:
            logger.warn('error, weather get fail')
            time.sleep(30 * 3)
            return

        weathers = r.json()['list']

        weather = filterNearstWeather(weathers, target_timestamp)

        logger.debug('{1}\'s weather is {0}'.format(weather, city))

        iconname = ICON_TABLE[weather['weather'][0]['icon']]

        image = Image.open(os.path.join(WEATHER_ICONS_DIRECTORY, iconname))

        if image is None:
            logger.warning("image is None.")
            time.sleep(30 * 3)
            return

    except requests.exceptions.ConnectionError as e:
        logger.exception(e)
        time.sleep(30 * 3)

    except KeyError:
        time.sleep(30 * 3)
        return

    logger.debug('start write icon.')

    for i in range(0, 300):
        if event.is_set():
            break

        drawAnimation(image, event)

    logger.debug('end of one cicle.')

def loop(event, city):
    unicornhathd.rotation(90)

    logger.debug('{} loop stert.'.format(city))
    while not event.is_set():
        main(event, city)

    logger.debug('{} loop end.'.format(city))

if __name__ == '__main__':
    """
    この書き方をしているのは
    これをライブラリとしてロードできるようにするため。
    ※ ただしimportエラーを修正しないと実行不可能
    https://docs.python.jp/3/library/__main__.html
    """

    # ロガーの設定
    # スクリプトとして動作する場合のみ出力ハンドラを追加する。
    from logging import StreamHandler, Formatter
    import sys

    # 環境変数DEBUGによってロギングレベルを変更する
    if os.environ.get('DEBUG', None):
        logger.setLevel('DEBUG')
    else:
        logger.setLevel('INFO')

    # StreamHandlerはそのまま標準出力として出力する。
    # つまりprint()と同様の動きをする
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s %(name)s %(message)s'))
    logger.addHandler(handler)

    logger.info('start application.')
    logger.info('city is %s', 'Setagaya')

    unicornhathd.brightness(0.5)
    unicornhathd.rotation(90)

    # ここがメイン処理。
    from threading import Event
    event = Event()
    # main()をひたすらループさせる。
    # finally
    try:
        while True:
            main(event, 'Setagaya')

    # Ctrl+C時に起きる例外を取得し、エラーメッセージが出ないようにする。
    except KeyboardInterrupt:
        logger.info('detect sigterm. goodbye.')

    # finallyは例外が出ようが出まいが終了時に必ず動作される。
    # ここでは、unicornhathdの終了処理を行わさせている。
    finally:
        unicornhathd.off()

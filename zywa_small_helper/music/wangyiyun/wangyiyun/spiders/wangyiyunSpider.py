# coding:utf-8
import traceback

from scrapy import Request, FormRequest
from scrapy.settings.default_settings import DEFAULT_REQUEST_HEADERS
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import re

from zywa_small_helper.music.wangyiyun.wangyiyun.items import MusicItem


class WangyiyunSpider(CrawlSpider):
    name = 'wangyiyun'
    # allowed_domains = ['music.163.com']
    allowed_domains = ["163.com"]
    base_url = 'https://music.163.com'

    # ids = ['1001']
    # initials = [65]

    ids = ['1001', '1002', '1003', '2001', '2002', '2003', '6001', '6002', '6003', '7001', '7002', '7003', '4001', '4002', '4003']
    initials = list(range(65, 91, 1))
    initials.append(0)

    def start_requests(self):
        for id in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url, id=id, initial=initial)
                yield Request(url, callback=self.parse_index)

    # 获得所有歌手的url
    def parse_index(self, response):
        artists = response.xpath('//*[@id="m-artist-box"]/li/div/a/@href').extract()
        for artist in artists:
            artist_url = self.base_url + '/artist' + '/album?' + artist[8:]
            yield Request(artist_url, callback=self.parse_artist)

    # 获得所有歌手专辑的url
    def parse_artist(self, response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)

    # 获得所有专辑音乐的url
    def parse_album(self, response):
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music

            yield Request(music_url, meta={'id': music_id}, callback=self.parse_music)

    # 获得音乐信息
    def parse_music(self, response):
        music_id = 'w' + response.meta['id']
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract()
        album = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()
        artist.sort()
        musicItem = MusicItem()
        musicItem['title'] = music
        musicItem['musicId'] = music_id
        musicItem['singers'] = artist
        musicItem['album'] = album
        musicItem['fromType'] = 2
        return musicItem
        # data = {
        #     'csrf_token': '',
        #     'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        #     'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
        # }
        # DEFAULT_REQUEST_HEADERS['Referer'] = self.base_url + '/playlist?id=' + str(music_id)
        # music_comment = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id)
        #
        # yield FormRequest(music_comment, meta={'id': music_id, 'music': music, 'artist': artist, 'album': album}, callback=self.parse_comment, formdata=data)

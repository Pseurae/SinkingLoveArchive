"""
MIT License

Copyright (c) 2021 Pseurae

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

###########################################################
#- VorbisComment Parser -----------------------------------
#- Made for learning about parsing metadata. --------------
###########################################################

import struct
import codecs
from io import BytesIO
import renpy.exports

class Vorbis(object):
    def __init__(self, file):
        self.file = renpy.exports.file(file).read()
        self.check_validity()

        self.comment_data = self.get_comment_data()
        self.comments = self.process_comment()

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        self.__comments = value

    def check_validity(self):
        magic_number = self.file[:4]
        if magic_number == b"OggS":
            return
        raise Exception ("Not a valid OGG file.")

    def get_comment_data(self):
        # Headers preciding the comments
        vorbis = b"\x03vorbis"
        opus = b'OpusTags'

        start = None

        if opus in self.file:
            start = self.file.find(opus) + len(opus)
        else:
            start = self.file.find(vorbis) + len(vorbis)
            
        if start or start != -1:
            return self.file[start:]

        raise Exception ("Can't determine the start of comments.")

    def process_comment(self):
        rv = {}

        with BytesIO(self.comment_data) as tagFile:
            vendor_length, = struct.unpack('I', tagFile.read(4))
            vendor = tagFile.read(vendor_length)
            rv["vendor"] = vendor

            tag_num, = struct.unpack('I', tagFile.read(4))
            for _ in range(tag_num):
                length, = struct.unpack('I', tagFile.read(4))

                try:
                    key_value = codecs.decode(tagFile.read(length), 'utf-8')
                except UnicodeDecodeError:
                    continue

                if "=" in key_value:
                    key, _, value = key_value.partition("=")
                    rv[key] = value

        return rv
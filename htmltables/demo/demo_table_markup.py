#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright © 2019 Arnold Reinders

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import pandas as pd
from htmltables import TableWriter

if __name__ == "__main__":
    image = open('/media/d/home/data/cats/train/cat.4.jpg', 'rb') #open binary file in read mode i
    image_read = image.read()
    image.close()

    with TableWriter ("table.html") as html:
        html.p('Writing a table the simple way')

        html.p('Without header colors')
        with html.Table(['i', 'i^2', 'i^3'], align=['left', 'right']) as tab:
            colors = ['red', 'yellow']
            html.p('Using tab.stripe(' + str(colors) + ')')
            for i in range (0, 11):
                tab.alt(colors).row([i, i**2, i**3])

        html.p("Next tables have hcolors=['yellow', 'teal']")
        with html.Table(['i', 'i^2', 'i^3'], align=['left', 'right'],
                        hcolors=['yellow', 'teal']) as tab:
            colors = ['red', 'yellow']
            html.p('Using tab.stripe(' + str(colors) + ')')
            for i in range (0, 11):
                tab.alt(colors).row([i, i**2, i**3])

        with html.Table(['i', 'i^2', 'i^3'], align=['left', 'right'],
                        hcolors=['yellow', 'teal']) as tab:
            colors = ['white', 'black', 'silver']
            html.p('Using tab.stripe(' + str(colors) + ')')
            for i in range (0, 11):
                tab.alt(colors).row([i, i**2, i**3])

        with html.Table(['i', 'i^2', 'i^3'], align=['left', 'right'],
                        hcolors=['yellow', 'teal']) as tab:
            colors = ['red', 'yellow', 'blue', 'aqua']
            html.p('Using tab.stripe(' + str(colors) + ')')
            for i in range (0, 11):
                tab.alt(colors).row([i, i**2, i**3])

        df = pd.DataFrame([[1,2,3],[10,11,12],[21,22,23],[31,32,33]],
                          index=['i1', 'i10', 'i20', 'i30'],
                          columns=['col-1', 'col-2', 'col-3'])
        html.p('Writing a DataFrame')
        html.write_dataframe(df, align=['left', 'right'],
                             hcolors=['black', 'white'],
                             colors=['white', 'black', 'silver'])

        html.p('Now writing a table the hard way')
        html.set_data (headers = ['i', 'i^2', 'i^3'])
        data = []
        for i in range(0, 11):
            data.append([i, i**2, i**3])

        html.set_data (data=data)
        html.p ("showing the results of the experiments")
        html.write_table (align="right", colors=["grey", "white"])

        html.p('Tabby the cat')
        html.write_img_inline(image_read, 'text', 'tag')

    print('Bye')

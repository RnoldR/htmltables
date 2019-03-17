"""
MIT License

Copyright (c) 2019 Arnold Reinders

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
import os
import base64
import matplotlib.pyplot as plt

class TableWriter(object):
    """ TableWriter writes html tables to file together with images and text

    It functions as a with item. It can only be called once because at __enter __
    a html header is written and at __exit__ an html footer.

    with TableWriter(...) as html:
        # write tables, images and text using the html file handle
    """
    HTMLFile = None

    class Table(object):
        """ Class Table creates an HTML table

        Method of use:

            with TableWriter(...) as html:
                with html.Table([list of headers], other parameters) as tab:
                    tab.row([list of row elements for row 1])
                       :
                    tab.row([list of row elements for row n])

        """
        def __init__(self, table_headers, align=["left"], hcolors=None):
            """ Initializes a table

            Args:
                table_headers (list of str): list of columns headers (str)
                align (list): list of alignments (str); should be len
                        (table_headers) long, when too few the last element
                        is repeated
                hcolors (list): [background, foreground] color of the header
                    in HTML code
            """
            self.table_headers = table_headers
            self.bg = "white" if hcolors is None else hcolors[0]
            self.fg = "black" if hcolors is None else hcolors[1]

            if align is None or align == []:
                align = ["left"]
            last = align[-1]
            for i in range(len(align), len(table_headers)):
                align.append(last)

            self.align = align
            self.rows = 0
            self.row_bg = "white"
            self.row_fg = "black"

            return

        def __enter__(self):
            """ Enters a Table

            Writes an HTML table header and writes the header itself.
            After this, successive calls to row can be made to add a row
            of data to the table.
            """
            TableWriter.HTMLFile.flush()
            TableWriter.HTMLFile.write ('<div class="Table">\n')
            TableWriter.HTMLFile.write ('<table style="border:1px solid black;border-collapse:collapse;">\n')
            TableWriter.HTMLFile.write ('   <tr>\n')
            TableWriter.HTMLFile.write ('   <font color="' + self.fg + '">\n')
            for i, cell in enumerate(self.table_headers):
                TableWriter.HTMLFile.write ('      <th align="' + self.align[i] +
                                    ' "style="border:1px solid black; background-color: ' +
                                    self.bg + '; color: ' + self.fg + '">')
                TableWriter.HTMLFile.write (str (cell))
                TableWriter.HTMLFile.write ('</th>\n')

            TableWriter.HTMLFile.write ('   </font>\n   </tr>\n')

            return self

        def __exit__(self, type, value, traceback):
            """ Writes the table footer.
            """
            TableWriter.HTMLFile.write ("</table>\n</div>\n")
            if traceback is not None:
                print(value, 'at line', traceback.tb_lineno)
                print('Crash:', traceback)

            return #self

        def row (self, row_list, align=None):
            """ Writes a row of data to the table in the html file

            Args:
                row_list (list of str): each element in the row is a row cell in the table
                align (list): list of alignments (str); should be len
                        (table_headers) long, when too few the last element
                        is repeated. When too many, remainder is ignored.
            Returns:
                self
            """
            if align is None:
                align = self.align
            TableWriter.HTMLFile.write ('   <tr>\n')
            for i, cell in enumerate(row_list):
                TableWriter.HTMLFile.write ('      <td align="' + align[i] + ' ' +
                                    '"style="border:1px solid black' +
                                    '; text-align: ' + str(align[i]) +
                                    '; background-color: ' +
                                    self.row_bg + '; color: ' + self.row_fg + '">')
                TableWriter.HTMLFile.write (str (cell))
                TableWriter.HTMLFile.write ('</td>\n')
            TableWriter.HTMLFile.write ('   </tr>\n')
            self.rows += 1

            return self

        def alt(self, colors=[]):
            """ Alternates fore- and background colors

            Alternates between bg,fg and alt_bg,alt_fg colors.
            When alt_bg,alt_fg are omitted they are the swapped bg,fg pair.
            Each even row written to the table the bg,fg pair is used,
            uneven alt_bg and alt_fg.
            When no alternation is desired let alt_bg, alt_fg be the same as
            bg, fg.

            Args:
                bg (str): background color of the header in HTML code
                fg (str): font color od the heading in HTML code
                alt_bg (str): alternative background color of the header in HTML code
                alt_fg (str): alternative font color od the heading in HTML code
            """
            if len(colors) < 2:
                return

            bg, fg, alt_bg, alt_fg = None, None, None, None
            if len(colors) >= 2:
                bg = colors[0]
                fg = colors[1]
                alt_fg = fg
                alt_bg = bg
                if len(colors) > 2:
                    alt_bg = colors[2]
                    alt_fg = fg
                if len(colors) > 3:
                    alt_fg = colors[3]

            if self.rows % 2 == 0:
                self.row_bg = bg
                self.row_fg = fg
            else:
                self.row_bg = alt_bg
                self.row_fg = alt_fg

            return self

    ## Class Table ##

    def __init__(self, file_name):
        """ Saves the file name of the html file as an attribute

        Args:
            file_name (str): name of the hrml file
        """
        self.file_name = file_name

        return

    def __enter__(self):
        """ Opens the file and writes an html header
        """

        TableWriter.HTMLFile = open (self.file_name, "w")
        self.headers = []
        self.data = []
        self.write_html_header ()

        return self

    def __exit__(self, type, value, traceback):
        """ Writes the html footer and closes the html file
        """
        if traceback is not None:
            print(value, 'at line', traceback.tb_lineno)
            print('Crash:', traceback)

        self.close()

        return #self

    def set_data (self, data=None, headers=None):
        """ Sets table data and header data if not None

        Args:
            data (table data): assigns data to self.data when not None
            headers (list of str): assigned to self.headers when not None
        """

        if data is not None: self.data = data
        if headers is not None: self.headers = headers

        return

    def write_html_header (self):
        """ Writes standard html header to file
        """

        s = '<html xmlns="http://www.w3.org/1999/xhtml">\n   <body>\n'\
            '      <div class="body-div" style="font-family: Sans-serif;">\n'
        TableWriter.HTMLFile.write (s)

        return

    def write_html_footer (self):
        """ Writes standard html footer to file
        """

        TableWriter.HTMLFile.write ("      </div>\n   </body>\n</html>")

        return

    def write_table_header (self, headers, align="left", bg="white", fg="black"):
        """ Write self.headers as table headers in the html file

        Args:
            * other parameters are assigned to table attributes
        """

        TableWriter.HTMLFile.write ('   <tr>\n')
        TableWriter.HTMLFile.write ('   <font color="' + fg + '">\n')
        for cell in headers:
            TableWriter.HTMLFile.write ('      <th align="' + align +
                                ' "style="border:1px solid black; background-color: ' +
                                bg + '; color: ' + fg + '">')
            TableWriter.HTMLFile.write (str (cell))
            TableWriter.HTMLFile.write ('</th>\n')
        TableWriter.HTMLFile.write ('   </font>\n   </tr>\n')

        return

    def write_table_row (self, row, align="left", bg="white", fg="black"):
        """ Writes a row of data to the table in the html file

        Args:
            row (list of str): each element in the row is a row cell in the table
            * other parameters are assigned to table attributes
        """

        TableWriter.HTMLFile.write ('   <tr>\n')
        for cell in row:
            TableWriter.HTMLFile.write ('      <td align="' + align + '" style="border:1px solid black;">')
            TableWriter.HTMLFile.write (str (cell))
            TableWriter.HTMLFile.write ('</td>\n')
        TableWriter.HTMLFile.write ('   </tr>\n')

        return

    def table_begin(self):
        TableWriter.HTMLFile.write ('<table style="border:1px solid black;border-collapse:collapse;">\n')

        return

    def table_end(self):
        TableWriter.HTMLFile.write ("</table>\n")

        return

    def write_header (self, align="left", bg="black", fg="white"):
        """ Write self.headers as table headers in the html file

        Args:
            * other parameters are assigned to table attributes
        """

        self.write_table_header(self.headers, align="left", bg="black", fg="white")

        return

    def write_table (self, align=["left"], hcolors=None, colors=["black", "white"]):
        """ Write self.data and self.headers as table to html file

        Args:
            * other parameters are assigned to table attributes
        """
        """
        self.table_begin()
        self.write_header (align=align, bg=bg, fg=fg)

        if self.data is not None:
            for row in range (0, len (self.data)):
                self.write_table_row (self.data[row], align=align)

        self.table_end()
        """
        with TableWriter.Table(self.headers, align=align,
                               hcolors=hcolors) as tab:
            if self.data is not None:
                for row in range (0, len (self.data)):
                    tab.alt(colors).row (self.data[row], align=align)

        return

    def write_dict(self, dict, headers=None, align=["left"],
                   hcolors=None, colors=["white","black"]):
        if headers is None:
            headers = ['Key', 'Value']

        with TableWriter.Table(headers, align=align,
                                        hcolors=hcolors) as tab:
            for key, value in dict.items():
                tab.alt(colors).row([key, value])

        return

    def write_dataframe(self, df, align=["left"], hcolors=None, colors=["white","black"]):
        self.headers = df.columns
        self.headers = self.headers.insert(0, '')
        with TableWriter.Table(self.headers, align=align,
                                        hcolors=hcolors) as tab:
            for row_index, row in enumerate(df.index):
                table_row = [str(row)]
                for cell in df.loc[row]:
                    table_row.append(str (cell))

                tab.alt(colors).row(table_row)

        return

    def p (self, text, tag='p'):
        """ Writes text to html file, between tags when tag is not ''
        """

        if tag == '':
            TableWriter.HTMLFile.write (text+'\n')
        else:
            TableWriter.HTMLFile.write ('<'+tag+'>'+text+'</'+tag+'>\n')

        return

    def write_img (self, image, text, fn, tag):
        """ Writes a link to an image file in the html file
        """

        w, h = image.size
        w = str(w)
        h = str(h)
        image.save(fn)
        self.p('<img src="'+fn+'" width="'+w+' height="'+h+'"></img>')
        self.p (text, tag)
        self.p ('<p> </p>')

        return

    def write_img_inline (self, image, text, tag):
        """ Writes an image inline as base64 to the html file
        """

        img = base64.b64encode(image).decode("utf-8")
        img_tag = '<img src="data:image/png;base64,{:s}" />'.format(img)
        self.p (text, tag)
        self.p(img_tag, '')
        #self.p ('<p> </p>')

        return

    def write_mat (self, image, text, fn, tag, size=None):#, fmt='jpg'):
        _, ext = os.path.splitext(fn)
        if len(ext) < 2:
            ext = 'png'
        else:
            ext = ext[1:]

        if size is None:
            w = str(image.shape[0])
            h = str(image.shape[1])
        else:
            w = str(size[0])
            h = str(size[1])

        plt.imsave(fn, image, format=ext)
        self.p('<img src="'+fn+'" width="'+w+' height="'+h+'"></img>')
        self.p(text, tag)
        self.p('<p>\t</p>')

        return

    def flush(self):
        TableWriter.HTMLFile.flush()

    def close (self):
        """ Writes html footer and closes html file
        """

        self.write_html_footer ()
        TableWriter.HTMLFile.close ()

        return

if __name__ == "__main__":
    print('*** <Please run the library "markup_table" from an applicatiom> ***')
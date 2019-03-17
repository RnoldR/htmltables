#TableMarkup#
This package makes is easy to create HTML files containing tables with images. I created it because I needed a way to log experiments in table form, often with pictures. 

To create a `htmltables` file:

~~~python
	from htmltables import TableWriter
	
	    with TableWriter(log_name) as logfile:
	    # Create tables, images and text via logfile
	    # Use p to write text to insert HTML text
	    
	    logfile.p('Heading 1', 'h1') # second argument is the HTML tag, defaults to `p`
	    logfile.p('Table 1 contains parameters and their values') 
	    # To create a table 
		with self.logfile.Table(['Parameter', 'Value'], hcolors=['gray', 'black']) as tab:
		
		    # Table has been created as tab, with two headers, 
		    # thereby indicating the number of columns (2)
		    # Now add columns with values. Convert to string 
		    # when necessary
		    tab.row(['Model type', str(model_types)])
		    tab.row(['Dropouts', str(dropouts)])
		    tab.row(['Batch sizes', str(batch_sizes)])
		    tab.row(['Epochs', str(epochs)])
		    tab.row(['GPU\'s', gpus])
		    tab.row(['Seq length', seqlen])
		    tab.row(['Training samples', n_train])
		    tab.row(['Validation samples', n_val])
~~~

Images can be inserted in two ways: via links and embedded.

###links###
Just add an HTML link to an image in the text, for example in the table row.

###Embedded###
Write the image to file and read  it. The following code  assumes that you have created an image file, for example a plot with `matplotlib`, and have saved this plot file file. The following code will insert this image in the HTML file as an embedded picture.

~~~python
 open(image_file_name, "rb") as image_file:
     im = image_file.read()
     logfile.write_img_inline(im, '', '')
~~~



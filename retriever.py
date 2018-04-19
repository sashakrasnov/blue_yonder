from sys import argv
import urllib.request as urq
import os

# Set this variable = `True` to process only image files. This option makes the script more universal
ONLY_IMAGES = True

# Looking for second parameter because argv[0] contains name of itself script
if len(argv) > 1:
    # Input file
    in_file = argv[1]

    # Directory to store downloaded files, will be current by default or if directory does not exist
    if len(argv) > 2 and os.path.exists(argv[2]):
        out_dir = os.path.abspath(argv[2])
    else:
        out_dir = os.path.abspath('.')

    # Trying to open file
    if(os.path.isfile(in_file)):
        with open(in_file, 'r', encoding='utf-8') as f:
            i = 1

            for url in f:
                # Removing new line symbols and other whitespaces
                u = url.strip()

                # URL may NOT contain any file extension or it may point to the script generating an image
                # So, to collect only images we need to know a mime type of the retrieved file
                # Also, any output to stdout will be separated by \t character to make easy processing in
                # spreadsheet programs or libraries like pandas when output of the script is redirected to a file
                try:
                    # Storing file in temporary folder (by default) and simultaneously get information about this file
                    # from the URL stored in `u` variable. Only checking mime type we may decide decline or not this file
                    temp_fn, info = urq.urlretrieve(u)

                    # So, lets check mime type to be sure this is an image file in case of ONLY_IMAGES is set True
                    if info.get_content_maintype() == 'image' or not ONLY_IMAGES:
                        # new filename with proper image file extension
                        out_fn = os.path.abspath(out_dir + '/' + str(i) + '.' + info.get_content_subtype())
                        os.rename(temp_fn, out_fn)

                        # Making next filename
                        i = i + 1

                        # Printing source URL according to the new filename
                        print(u + '\t', out_fn)

                    # Removing temporary non-image file
                    else:
                        os.remove(temp_fn)
                        print(u + '\t\tNot an image!')

                except urq.URLError:
                    print(u + '\t\tError retriving!')

    else:
        print('Cannot open file "' + in_file + '". File not found or it is not a file.')

# Help information
else:
    print('Usage: python', argv[0], '<input_file> <output_dir>')
    print('<input_file> is a plaintext file containing URLs, one per line.')
    print('[output_dir] directory to store downloaded content. If omitted or directory does not exist, the current directory will be used.')

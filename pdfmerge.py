import glob
import PyPDF2
import sys
import os
import optparse
import datetime

if __name__=='__main__':

    #FOR DEBUG PURPOSES:
    #sys.argv = ['C:/pdf-join.py', raw_input('Enter Path:'), raw_input('Enter destination filename:')]
    sys.argv = ['C:/pdf-join.py', '-p', 'C:\Mayer']#, '-v']

    parser = optparse.OptionParser()

    parser.add_option('-d', '--dest',
        action="store",
        dest="dest",
        help="Destination merged file",
        default='merged_{0}.pdf'.format(datetime.datetime.now().strftime("%y%m%d_%H%M%S")))

    parser.add_option('-p', '--path',
        action="store",
        dest="path",
        help="Source path",
        default='None')

    parser.add_option('-v', '--verbose',
        action="store_true",
        dest="v",
        help="Show verbose messages",
        default=False)

    options, args = parser.parse_args()

    if options.path=='None':
        print "ERROR: Source path must be declared.\n"
        print parser.format_help()
        sys.exit(1)

    path = options.path
    dest = options.dest
    v = options.v

    

    file_list = [f for f in os.listdir(path) if '.pdf' in f]
    if v: print "PDF files in {0}:\n\n{1}".format(path,file_list)
    
    if len(file_list)==0:
        print "no PDF files in {0}, what are you trying to do?!".format(path)
        sys.exit(1)
    

    pages = 0
    main_pdf = PyPDF2.PdfFileMerger()
    for filename in file_list:
        if v: print "Working on: {0}".format(filename)
        cur = PyPDF2.PdfFileReader(os.path.join(path,filename)) # no need to close this object (also has no _exit_)
        main_pdf.append(cur)
        pages += cur.getNumPages()        


    out_dir = os.path.join(path, 'merged')
    if not os.path.exists(out_dir):
        if v: print "Creating dir - \'merged\'"
        os.makedirs(out_dir)
        
    main_pdf.write(os.path.join(out_dir,dest))
    print "File successfully saved to: {0} ({1} pages)".format(os.path.join(out_dir,dest),pages)
    print "Cya."
    
        

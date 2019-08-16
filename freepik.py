import os, sys, getopt, shutil
import zipfile, tempfile


def extract_zip(dst_dir, types, z_file):
    try:
        count = 0
        prefix = z_file.split('.zip')[0]
        with zipfile.ZipFile(z_file, 'r') as zip_file:
            for img in zip_file.namelist():
                if img.endswith(tuple(types)):
                    zip_file.extract(img, tempfile.gettempdir())
                    shutil.copy(
                        tempfile.gettempdir() + '/' + img,
                        dst_dir + '/' + os.path.basename(prefix) + '-' + img
                    )
                    os.remove(tempfile.gettempdir() + '/' + img)
                    # old code below - remove later
                    # os.rename(tempfile.gettempdir() + '/' + img, dst_dir + '/' + os.path.basename(prefix) + '-' + img)
                    count+=1
    except zipfile.BadZipFile as e:
        print('{0} is a Bad Zip File: {1}'.format(z_file, str(e)))
        return False
    else:
        if count == 0:
            print('ZipFile: {} did not contain any images to process.'.format(z_file))
        return True


def check_args(argv):
    # Check arguments
    try:
        opts, args = getopt.getopt(argv, "hs:d:t:", ["source=", "destination=", "type="])
    except getopt.GetoptError:
        print('freepik.py -s <source directory> -d <destination directory> -t <type|type...>')
        sys.exit(2)
    else:
        if not opts:
            print('freepik.py -s <source directory> -d <destination directory> -t <type|type...>')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('Usage: ext_from_zip.py -s <source directory> -d <destination directory> -t <type|type...>')
                sys.exit()
            elif opt in ("-s", "--source"):
                src_dir = arg.strip().replace('\\','')
            elif opt in ("-d", "--destination"):
                dst_dir = arg.strip().replace('\\','')
            elif opt == "-t" or opt == "--type":
                file_types = arg.strip().lower().split('|')

        # argv validations
        if not os.path.isdir(src_dir):
            print('The source directory {} does not exist !, respecify...'.format(src_dir))
            sys.exit()
        elif not os.path.isdir(dst_dir):
            print('The destination directory {} does not exist !, attempting to create...'.format(dst_dir))
            os.mkdir(dst_dir)
            print('created...')
        elif not file_types:
            print('No file types were specified for extraction.')
            sys.exit()

        params = {'src_dir': src_dir, 'dst_dir': dst_dir, 'file_types': file_types}
        return params


def zip_files(path):
    # Generator object for all files present in source path
    for file in os.listdir(path):
        if file.endswith(".zip") and os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)


def process_zip_files(params):
    ''' Fetch each zip file and process to catch the relevant information. '''
    ccount=0
    tcount=0
    bcount=0
    bad_zip_list = []
    for file in zip_files(params['src_dir']):
        tcount+=1
        status = extract_zip(params['dst_dir'], params['file_types'], file)
        if status:
            # print('File {} was processed successfully.'.format(file))
            ccount+=1
        else:
            print('File {} was NOT processed successfully.'.format(file))
            bad_zip_list.append(os.path.basename(file))
            bcount+=1
    print('Total Zip Files In Queue: {}'.format(tcount))
    print('Total Zip Files Processed: {}'.format(ccount))
    print('Total Bad Zip Files Encountered: {}'.format(bcount))
    print('Bad Zip Files: {}'.format(bad_zip_list))


if __name__ == '__main__':
    params = check_args(sys.argv[1:])
    os.chdir(params['src_dir'])
    # loop through all files and then
    process_zip_files(params)

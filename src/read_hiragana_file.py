import zipfile
import struct
import random
import os
import numpy as np
from PIL import Image, ImageEnhance

sz_record     = 8199  # Number of bytes in each record (http://etlcdb.db.aist.go.jp/etlcdb/etln/form_e8g.htm for details)
raw_data_dir  = 'raw'

def relative_path(path):
    return os.path.dirname(os.path.realpath(__file__)) + '/' + path

def extract_zip():
    zip_files = []
    for file in os.listdir('./'):
        if file.endswith(".zip"):
            zip_files.append(os.path.join('./', file))

    if zip_files:
        for file in zip_files:
            output_dir = relative_path('{}/{}'.format(raw_data_dir, os.path.splittext(file)))

            if not os.path.exists(output_dir):
                print ('Extracting {}/{}...'.format(raw_data_dir, file))

            with zipfile.ZipFile(relative_path('{}/{}'.format(raw_data_dir, file)), 'r') as file:
                file.extractall(relative_path(raw_data_dir))

            print ('raw/{} extracted!'.format(file))
    else:
        print ('No zip files exist. Skipping')

def read_record_ETL8G(f):
    s = f.read(sz_record)
    r = struct.unpack('>2H8sI4B4H2B30x8128s11x', s)
    iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
    iL = iF.convert('L')
    return r + (iL,)

def read_hiragana():
    output_file = 'hiragana.npz'
    # hiragana_total = 72, dataset_total = 160, y = 127, x = 128
    array = np.zeros([72, 160, 127, 128], dtype=np.uint8)

    folders = ([x[0] for x in os.walk(raw_data_dir)])

    for folder in folders[1:]:
        print ('Scanning through {}'.format(folder))
        number_of_files_to_process = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]) - 2

        for file_index in range(1, number_of_files_to_process+1):
            filename = './{}/ETL8G_{:02d}'.format(folder, file_index)
            with open(filename, 'rb') as f:
                for id_dataset in range(5): # 5 datasets per file
                    moji = 0
                    dataset_size = 956      # 956 categories per dataset
                    for i in range(dataset_size):
                        r = read_record_ETL8G(f)
                        if b'.HIRA' in r[2]:
                            array[moji, (file_index - 1) * 5 + id_dataset] = np.array(r[-1])
                            moji += 1
                        print ('Unpacking dataset {}/{} - {}% ...'.format(file_index, number_of_files_to_process, int((float(i) / dataset_size) * 100)))

        print ('Scanning of {} is done. Next...'.format(folder))

    print ('All data beed processed. Saving into {}'.format(output_file))
    np.savez_compressed(output_file, array)

def main():
    extract_zip()
    read_hiragana()

main()


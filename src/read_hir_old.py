import struct
import numpy as np
from PIL import Image

sz_record = 8199


def read_record_ETL8G(f):
    dataset = f.read(sz_record)
    result  = struct.unpack('>2H8sI4B4H2B30x8128s11x', dataset)
    print ('{} <--> {}'.format(result[1], result[2]))

    iF = Image.frombytes('F', (128, 127), result[14], 'bit', 4)
    iL = iF.convert('L')

    return result + (iL,)


def read_hiragana():
    # Character type = 72, person = 160, y = 127, x = 128
    array = np.zeros([72, 164, 127, 128], dtype=np.uint8)

    for j in range(1, 2):
        filename = './raw/ETL8G/ETL8G_{:02d}'.format(j)
        with open(filename, 'rb') as f:
            print ('Reading {}'.format(filename))
            for id_dataset in range(5):
                moji = 0
                print ('Dataset #{}'.format(id_dataset))
                for i in range(956): #956
                    r = read_record_ETL8G(f)
                    # print (r[2].strip())
                    if b'.HIRA' in r[2]:
                        # print (r[2])
                        array[moji, (j - 1) * 5 + id_dataset] = np.array(r[-1])
                        moji += 1
                # print (moji)
    np.savez_compressed("hiragana.npz", array)

read_hiragana()

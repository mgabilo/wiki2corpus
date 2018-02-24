#!/usr/bin/python
import sys
import pdb

def main():
    sys.stdout.write('Name of corpus: ')
    filename = sys.stdin.readline().strip()
    sys.stdout.write('Size of parts in GB: ')
    bytes_per_part = int(float(sys.stdin.readline().strip()) * (1024.0 ** 3))
    sys.stdout.write('Base file prefix: ')
    prefix = sys.stdin.readline().strip()

    print bytes_per_part

    fin = open(filename)
    part_number = 0
    split_ready = False
    fout_part = open(prefix + '-' + str(part_number), 'w')

    for line in fin:
        byte_pos = fout_part.tell()
        if byte_pos > bytes_per_part:
            split_ready = True

        if split_ready and line.startswith('** Article:'):
            part_number += 1
            fout_part.close()
            fout_part = open(prefix + '-' + str(part_number), 'w')
            split_ready = False

        fout_part.write(line)
    fout_part.close()
    fin.close()

if __name__ == "__main__":
    main()

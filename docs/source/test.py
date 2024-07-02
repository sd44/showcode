import pathlib
import sys

src1_dir = pathlib.Path(__file__).parents[1].resolve() / 'src/showcode'
print(f'{src1_dir}')

src_dir = pathlib.Path(__file__).parents[2].resolve() / 'src/showcode'
print(f'{src_dir}')

import argparse, subprocess, json, os
from vol_paths import paths

parser = argparse.ArgumentParser(prog='partial_extract.py',
                                 description='extract features in chunks')

# parser.add_argument('--pkgs-index', '-pi', dest='pkgs_index', type=str)
# parser.add_argument('--config', '-c', dest='config', type=str)
# parser.add_argument('--prev-fm', '-fm', dest='prev_fm', type=str)
# parser.add_argument('--stats', '-s', dest='stats', type=str)

parser.add_argument('--chunk-size', '-cs', dest='chunk_size', type=int, required=True)
parser.add_argument('--max-bins', '-mb', dest='max_bins', type=int, required=True)
parser.add_argument('--timeout', '-t', dest='timeout', type=int, required=True)

def get_num_pkgs(pkgs_index):
  f = open(pkgs_index)
  arr = json.load(f)
  size = len(arr)
  f.close()
  return size

def init_fm(fm_file):
  f = open(fm_file, 'w+')
  f.write('[]')
  f.close()

def main():
  args = parser.parse_args()
  pkgs_index = os.path.join(paths['pkgs'], 'packages.json')
  num_pkgs = get_num_pkgs(pkgs_index)

  init_fm(paths['ftr_map'])
  
  pkg_ind = 0
  chunk_ind = 1
  while pkg_ind < num_pkgs:
    print(f'[info] starting chunk {str(chunk_ind)}')
    run_info = subprocess.run(['/DelphiCpp/build/dcpp_extract',
                               '-p', pkgs_index,
                               '-c', paths['conf'],
                               '-fm', paths['ftr_map'],
                               '-s', os.path.join(paths['log_dir'], 'time_log' + str(pkg_ind) + '.json'),
                               '-l', os.path.join(paths['log_dir'], 'extract.log'),
                               '-cs', str(args.chunk_size),
                               '-pi', str(pkg_ind),
                               '-t', str(args.timeout)])
    if run_info.returncode != 0:
      print('[info] failed on chunk ' + str(chunk_ind))
    else:
      print(f'[info] finished chunk {str(chunk_ind)}')
    pkg_ind += args.chunk_size
    chunk_ind += 1

main()

from utils import execute, ArgParseImpl

def _compare_goldens(render_results, output_dir, goldens):
  for result in render_results:
    if result['result'] != RESULT_OK:
      continue

    out_tif_basename = f"{result['name']}.tif"
    out_tif_name = f'{output_dir}/{out_tif_basename}'
    golden_path = goldens.get(out_tif_basename)
    if not golden_path:
      result['result'] = RESULT_FAILED_NO_GOLDEN
      result['result_code'] = 1
    elif not same_image(golden_path, out_tif_name):
      result['result'] = RESULT_FAILED_IMAGE_DIFF
      result['result_code'] = 1
  return render_results

if __name__ == '__main__':
  parser = ArgParseImpl()
  parser.add_argument('--src', help='Directory of the base of the diff.', required=True)
  parser.add_argument('--dest', help='Directory of the comparison of the diff.')
  parser.add_argument('--out', help='Directory of output for the result of the diff.')

  args, _ = parser.parse_known_args(sys.argv[1:])

  dest = args.dest
  if not dest:
    print('Assume the default renderdiff output folder')
    dest = os.path.join(os.getcwd(), './out/renderdiff_tests')
  assert os.path.exists(dest), f"Destination folder={dest} does not exist."
  
  goldens = {
    os.path.basename(fpath) : fpath for fpath in \
    glob.glob(f'{os.path.join(tmp_golden_dir, test.name)}/**/*.tif', recursive=True)
  }
  results = compare_goldens(results, output_dir, goldens)
  

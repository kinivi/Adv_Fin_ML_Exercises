import os
import datetime as dt
import argparse


def fix_file(fp_in_, fp_out_):
	if not os.path.exists(fp_in_):
		print('File "{}" does not exist'.format(fp_in_))
	else:
		with open(fp_in_, 'r') as file_in:
			all_lines = file_in.readlines()
			if len(all_lines) > 0:
				head_line = '{},date, weekday\n'.format(all_lines[0].rstrip('\n'))
				with open(fp_out_, 'w') as file_out:
					file_out.write(head_line)
					for line in all_lines[1:]:
						parts = line.split(',')
						if len(parts) > 0:
							utc_dt = dt.datetime.fromtimestamp(float(parts[0]) / 1000.0, tz=dt.timezone.utc)
							file_out.write('{},{},{}\n'.format(
								line.rstrip('\n'),
                				utc_dt.strftime("%Y-%m-%d %H:%M:%S"),
								utc_dt.weekday()
							))
						else:
							print('Row is empty, file: "{}"'.format(fp_in_))
			else:
				print('File "{}" is empty'.format(fp_in_))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process file')
	parser.add_argument('--filename', metavar='-f', type=str,
					help='filename to proceed')


	args = parser.parse_args()
	
	files_to_fix = [
		args.filename
	]

	base = os.path.dirname(__file__)
	for fp in files_to_fix:
		fix_file(
			os.path.join(base, fp),
			os.path.join(base, 'new_{}'.format(fp))
		)

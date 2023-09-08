import re
import functools
import subprocess
import dataclasses



@dataclasses.dataclass(frozen = False, kw_only = False)
class Tags:

	data : bytes

	class ValueError(ValueError):
		pass

	def __post_init__(self):

		if not self.data:
			raise Tags.ValueError('No data provided (empty bytes object)')

		if (
			errors := subprocess.run(
				args = (
					'ffmpeg',
					'-v', 'error',
					'-i', '-'
					'-f', 'null',
					'-'
				),
				input          = self.data,
				capture_output = True
			).stdout.decode()
		):
			raise Tags.ValueError(f'ffmpeg have errors checking data: {errors}')

	def __getitem__(self, key: str):
		try:
			return str(
				next(
					re.finditer(
						f'TAG:{key}=(.+)',
						subprocess.run(
							args = (
								'ffprobe',
								'-v', 'quiet',
								'-show_entries',
								f'format_tags={key}',
								'-'
							),
							input          = self.data,
							capture_output = True
						).stdout.decode()
					)
				).groups()[0]
			)
		except (IndexError, StopIteration) as exception:
			raise KeyError from exception

	def __call__(self, **tags: str):
		return Tags(
			subprocess.run(
				args = (
					'ffmpeg',
					'-i', '-',
					'-map', '0',
					'-y',
					'-codec', 'copy',
					'-write_id3v2', '1',
					*(
						element
						for pair in (
							('-metadata', f'{key}={value}')
							for key, value in tags.items()
						)
						for element in pair
					),
					'-f', 'mp3',
					'-',
				),
				input          = self.data,
				capture_output = True
			).stdout
		)

	@functools.cached_property
	def cover(self):
		return subprocess.run(
			args = (
				'ffmpeg',
				'-v', 'quiet',
				'-i', '-',
				'-an', '-vcodec', 'copy',
				'-f', 'mjpeg',
				'-'
			),
			input          = self.data,
			capture_output = True
		).stdout or None
import re
import datetime
import functools
import subprocess
import dataclasses

from .Media import Media



@dataclasses.dataclass(frozen = False, kw_only = False)
class Tags:

	source : Media

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
							input          = self.source.data,
							capture_output = True
						).stdout.decode()
					)
				).groups()[0]
			)
		except (IndexError, StopIteration) as exception:
			raise KeyError from exception

	def __call__(self, **tags: str):
		return Tags(
			Media(
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
					input          = self.source.data,
					capture_output = True
				).stdout
			)
		)

	@functools.cached_property
	def artist(self):
		return self['artist']

	@functools.cached_property
	def album(self):
		return self['album']

	@functools.cached_property
	def title(self):
		return self['title']

	@functools.cached_property
	def date(self):
		return datetime.datetime.fromisoformat(self['date'])

	@functools.cached_property
	def duration(self):
		hours, minutes, seconds = re.findall(
			r'time=(\d+):(\d+):(\d+\.\d+)',
			subprocess.run(
				args = (
					'ffmpeg',
					'-i', '-',
					'-f', 'null',
					'-'
				),
				input          = self.source.data,
				capture_output = True
			).stderr.decode()
		)[-1]
		return (int(hours) * 60 + int(minutes)) * 60 + float(seconds)

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
			input          = self.source.data,
			capture_output = True
		).stdout or None

	# def covered(self, cover: bytes):
	# 	return Tags(
	# 		subprocess.run(
	# 			args = (
	# 				'ffmpeg',
	# 				'-i', '-',
	# 				'-i', '-', -map 0:a -map 1 -codec copy -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" -disposition:v attached_pic output.flac
	# 			),
	# 			input = self.data,
	# 			capture_output = True
	# 		).stdout
	# 	)
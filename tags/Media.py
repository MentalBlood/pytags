import subprocess
import dataclasses



@dataclasses.dataclass(frozen = True, kw_only = False)
class Media:

	data : bytes

	class ValueError(ValueError):
		pass

	def __post_init__(self):

		if not self.data:
			raise Media.ValueError('No data provided (empty bytes object)')

		if (
			errors := subprocess.run(
				args = (
					'ffmpeg',
					'-v', 'error',
					'-i', '-',
					'-f', 'null',
					'-'
				),
				input          = self.data,
				capture_output = True
			).stderr.decode()
		):
			raise Media.ValueError(f'ffmpeg have errors checking data: {errors}')

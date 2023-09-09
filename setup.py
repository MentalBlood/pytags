import pathlib
import setuptools



if __name__ == '__main__':

	setuptools.setup(
		name                          = 'pytags',
		version                       = '0.1.0',
		description                   = 'Interface to ffmpeg tagging abilities',
		long_description              = (pathlib.Path(__file__).parent / 'README.md').read_text(),
		long_description_content_type = 'text/markdown',
		author                        = 'mentalblood',
		packages                      = setuptools.find_packages(exclude = ['tests*']),
		install_requires              = []
	)
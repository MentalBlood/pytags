import pytest
import pathlib
import functools

from .. import tags



@functools.lru_cache
def audio():
	return tags.Tags(tags.Media(pathlib.Path('test.mp3').read_bytes()))


@pytest.mark.parametrize(
	'key',
	(
		'artist',
		'album',
		'title',
		'composer'
	)
)
def test_getitem(key: str):
	assert audio()[key]


@pytest.mark.parametrize(
	'key',
	(
		'artist',
		'album',
		'title',
		'composer'
	)
)
def test_set(key: str, value: str = 'value'):
	assert audio()(**{key: value})[key] == value


def test_nonexistent_key():
	with pytest.raises(KeyError):
		audio()['nonexistent_key']


def test_invalid_data():
	with pytest.raises(tags.Media.ValueError):
		tags.Media(b'invalid_data')
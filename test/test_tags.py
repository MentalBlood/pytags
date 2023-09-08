import pytest
import pathlib
import functools

from .. import tags



@functools.lru_cache
def audio():
	return tags.Tags(pathlib.Path('test.mp3').read_bytes())


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
		assert audio()['nonexistent_key']
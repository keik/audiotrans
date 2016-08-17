# audiotrans

[![License](https://img.shields.io/pypi/l/audiotrans.svg?style=flat-square)](https://github.com/keik/audiotrans/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/audiotrans.svg?style=flat-square)](https://pypi.python.org/pypi/audiotrans)
[![PyPI](https://img.shields.io/pypi/v/audiotrans.svg?style=flat-square)](https://pypi.python.org/pypi/audiotrans)
[![Travis CI](https://img.shields.io/travis/keik/audiotrans.svg?style=flat-square)](https://travis-ci.org/keik/audiotrans)
[![Coverage Status](https://img.shields.io/coveralls/keik/audiotrans.svg?style=flat-square)](https://coveralls.io/github/keik/audiotrans)

Transform audio in real-time.


## Installation

audiotrans use [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) which depends [PortAudio](http://www.portaudio.com/). So we have to install PortAudio in ways of each platformas.

Then

```
pip install audiotrans
```

Now we can use `audiotrans` command.


### Installation transform modules

audiotrans is plugin based architecture. To transform audio, we have to install and use transform modules.

Transform modules like of the below is available.

* [audiotrans-transform-fft](https://github.com/keik/audiotrans-transform-fft)
* [audiotrans-transform-stft](https://github.com/keik/audiotrans-transform-stft)
* [audiotrans-transform-istft](https://github.com/keik/audiotrans-transform-istft)


## Usage

```
usage: audiotrans [-h] [-v] [-b BUFFER_SIZE] [-t TRANSFORMS] [-c CHART_TYPE]
                  [filepath]

Transform audio in real-time

positional arguments:
  filepath              Audio file path to read on stream and transform.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Run as verbose mode
  -b BUFFER_SIZE, --buffer-size BUFFER_SIZE
                        Buffer size to read data on stream
  -t TRANSFORMS, --transform TRANSFORMS
                        Transform module name to apply.
                        Specified module name is auto-prefixed `audiotrans_transform_`,
                        so to use `audiotrans_transform_stft`, you may just specify `stft`.
  -c CHART_TYPE, --chart-type CHART_TYPE
                        Chart type to data visualization.
                        Below values are available:

                          freq : Display frequency of wave.
                                 To plot, transformed data must be formed 1-D array of wave.
                          spec : Display spectrum of wave.
                                 To plot, Transformed data must be formed 1-D array of spectrum
                                 or 2-D array of spectrogram.

                        Or if not specified, no chart appears.

Passing arguments to transforms:
  For -t, you may use subarg syntax to pass options to the transforms
  as the second parameter. For example:

    -t [ stft -w 2048 -H 256 ]

  For details of available options, see documents of transforms which to use.
```


## Test

```
make test
```


## License

MIT (c) keik

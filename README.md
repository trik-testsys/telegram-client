[![CodeFactor](https://www.codefactor.io/repository/github/trik-testsys/telegram-client/badge)](https://www.codefactor.io/repository/github/trik-testsys/trik-testsys-telegram-client)
<a href="https://github.com/trik-testsys/telegram-client/"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<a href="https://github.com/trik-testsys/telegram-client/actions"><img alt="Actions Status" src="https://github.com/trik-testsys/trik-testsys-telegram-client/actions/workflows/lint.yml/badge.svg"></a>
# Grading system client for TRIK studio

## Overview
Grading system client for TRIK studio, which allows to send task to test and view results.

## Install and Run

### With docker
1. Build image:
`docker build .`
2. Put dirs with tasks, logs and secrets alongside with project directory, or edit config.py before building image 
3. Run bot:
`docker run 'your_image_id''`

### Without docker
1. Install dependencies:
`pip3 install -r requirements.txt`
2. Put dirs with tasks, logs and secrets alongside with project directory or edit settings in **config.py** file
3. Run bot:
`python3 main.py`

## Code Style
In this project we use [CodeFactor](https://www.codefactor.io) and [flake8](https://github.com/PyCQA/flake8) to check code style. 
[Black](https://github.com/psf/black) for formatting.

## Contributing
Please, follow [Contributing](CONTRIBUTING.md) page.

## Authors
* Viktor Karasev - [KarasssDev](https://github.com/KarasssDev)

## License
This project is Apache License 2.0 - see the [LICENSE](LICENSE) file for details

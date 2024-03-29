# The IEC 62320 Python Package

# Description

The IEC 62320 Python Package implements parts of the IEC 62320 series of standards,  'Maritime navigation and radiocommunication equipment and systems - Automatic identification system (AIS)'. Currently, support is included for the following parts:

* Part 1, 'AIS Base Stations - Minimum operational and performance requirements, methods of testing and required test results'.

The package has been developed using Python v.3.11.1.

## Installation

1. Ensure [Python](https://www.python.org/downloads/) and the [PDM](https://pdm-project.org/) dependency manager are installed.

1. Clone the GRAD `py_iec_62320` repository.
    ```
    git clone https://github.com/gla-rad/py_iec_62320.git
    ```

1. Navigate to the local repository.
    ```
    cd py_iec_62320
    ```

1. Install the IEC 62320 package and its dependencies from the `pdm.lock` file.
    ```
    pdm sync --prod
    ```
    Upon successful execution of the above command, `pdm` will generate a virtual Python environment in `./.venv/` and install the package along with its required dependencies into it in *production mode*.

## Code Usage

The main modules of the IEC 62320 package are located under `./src/iec_62320/`. The code is structured as outlined below.

For examples of usage, see the source code in this repository and the repositories linked under 'Related Projects'.

### Subpackage: `part_1`

#### Module: `sentences.py`

This module contains classes for representing, generating and, in the future, parsing
presentation interface sentences compliant with the IEC 62320-1:2015 standard. Currently, support has been implemented for the following sentence formatters:
* TSA, 'Transmit slot assignment'.

## Contributing

We welcome contributions! If you wish to contribute to this project, please follow these steps:

1. Fork the repository and create a new branch.
1. Clone your repository to your local machine.

    ```
    git clone <your_repository_address>
    cd py_iec_62320
    ```
1. Install the package in *development mode* using PDM.
    ```
    pdm sync --dev
    ```

    Note: The development installation includes dependencies for the [Spyder IDE](https://www.spyder-ide.org/), which may not be necessary if you are using a different IDE.
1. Make your changes and test thoroughly.
1. Submit a pull request with a clear description of your changes.

## Tests

This is currently work in progress.

Unit test modules are expected to be located under `./tests/`. The chosen testing framework for this project is [pytest](https://pytest.org), included as part of the development installation.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](./LICENSE) file for details.

## Support

Email: Jan.Safar@gla-rad.org

Issue Tracker: [GitHub Issues](https://github.com/gla-rad/py_iec_62320/issues)

## Related Projects

### Python

* [Rec. ITU-R M.1371 package](https://github.com/gla-rad/py_rec_itu_r_m_1371.git)
* [IEC 61162 package](https://github.com/gla-rad/py_iec_61162.git)
* [IEC PAS 63343 package](https://github.com/gla-rad/py_iec_pas_63343.git)
* [VDES1000 package](https://github.com/gla-rad/py_vdes1000.git)

### Java

* VDES1000 Library - a Java port of this package, used within the GRAD [e-navigation service framework](https://github.com/orgs/gla-rad/repositories?q=enav) (source code is not yet publicly available).

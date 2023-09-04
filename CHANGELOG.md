<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Extraneous mouse movement exits wake sequence.
- Popup shown during wake sequence.

### Changed

- Reduced dependencies to minimum, and version >1.0+

## [3.0.0] - 2023-09-04

### Added

- Keyboard presses count as active
- Added requirements file (use `pip install -r requirements.txt` to install dependencies)

### Fixed

- Mouse didn't return to original idle position, now it does.

## [2.0.0] - 2023-08-09

### Added

- Command line arguments to control script behaviour including logging, time between mouse movements, and whether to move mouse between screens.
- Better documentation (README.md and within code), added CHANGELOG.md.

### Changed

- Logging to file and printing to stdout disabled by default (enable with cmd line arg --log). Startup message still printed to stdout.
- Mouse movements occur on screeen mouse is idle on (enable with cmd line arg --multiscreen). When disabled, mouse movements occur on primary screen only, as per version 1.1.0.
- Mouse returns to original position after movement.

## [1.1.0] - previously version 2023-07-24c

### Added

- Option to exit wake sequence early by pressing ```Esc```.

### Changed

- Removed '-log' from log file name. (Don't know why I did that.)

### Fixed

- Idle time reset by keyboard activity, as well as mouse activity.

## [1.0.0] - 2023-01-27

- Initial release

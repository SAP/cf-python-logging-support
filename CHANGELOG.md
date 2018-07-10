# Change Log
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](http://semver.org/).

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## 4.0.1 - 2018-07-10

### Fixed

 - Log error throws an exception

## 4.0.0 - 2018-07-04

### Added
 - Log exception stacktrace

### Changed
 - Incompatible change: removed `log` function from request in falcon support

## 3.3.1 - 2018-06-18

### Fixed
 - Correlation ID should be thread safe

## 3.3.0 - 2018-06-07

### Added
 - Support set and get correlation ID

## 3.2.0 - 2018-05-31

### Added
 - Support for Falcon web framework

### Changed
 - Hide sensitive fields by default

### Fixed
 - Do not apply JSON formatting on unknown LogRecord

## 3.1.1 - 2018-03-06

### Fixed
 - Fix missing sap namespace in response readers

## 3.1.0 - 2018-01-04

### Changed
 - Introduced sap namespace

## 3.0.1 - 2017-12-11

### Changed
 - Improved documentation

## 3.0.0 - 2017-11-16

### Changed
 - Improved JSON logging
 - Simplified integration with Flask applications
 - Simplified integration with Sanic applications
 - Cleanup for open-sourcing

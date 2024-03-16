# pypoller

## Overview

pypoller is a lightweight and easy-to-use framework for polling a resource at regular intervals and providing notifications on any updates. It is designed to simplify the process of monitoring a remote service for changes and alerting users or systems when relevant updates occur.

Detailed docs available at https://www.mohitc.com/pypoller/docs/

## Features

- **Polling**: The library allows you to define a polling interval, specifying how frequently the service should be checked for updates.

- **Notifications**: When a change is detected in the service, the library supports customizable notification mechanisms. Currently messaging via Twilio is implemented.

- **Configurability**: The library is highly configurable and extensible. Adding support for any notification mechanism or resource should be seamless.
## Installation

`pip install .`

For playwrigt (US Visa):

`playwright install`

## Usage
Refer to examples to learn how to use the library.

To provide twilio credentials for twilio, create a `.env` file by copying the `.env.sample` file, and replace the placeholder twilio parameters to enable notifications via SMS.
If twilio credentials are not provided, notifications will be printed to console.

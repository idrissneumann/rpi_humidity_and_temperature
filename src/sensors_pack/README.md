# Sensor pack

In essence, the sensor pack module contains the different sensors' _drivers_.

## What is a driver?

A driver is an interface that retrieves the readings of a certain sensor.

## Why use 'drivers' instead of directly accessing the readings?

We use the drivers system to allow for future modularity within the project as well as to guarantee a level of consistency between the readings of different sensors that serve the same purpose but are from different providers.
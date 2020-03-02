# Take home assignment for Python

## Let's Build a Vendor Availability system

## Problem

We need to know if a vendor (restaurant) is available to deliver a meal.
So given a list of upcoming meals, build a function that will tell us if
the vendor (restaurant) is available to take the order.

## Requirements

- input: take a vendor_id and a date
- output: True if the vendor is available, False if not
- A vendor is available if:
  - They have enough drivers for a concurrent delivery
  - As long as the delivery blackout period doesn't overlap (30 minutes before for delivery and setup, and 10 minutes after for returning back)

## Pre Requisites

Make sure you have `pytest` installed

```
pip install -U pytest
```

## To Run

```
python main.py
```

## Notes & Assumptions

- I assumed that the vendors & meals dict will not have any missing data/keys. Alternatively, could handle & raise KeyErrors

- I added some more sample data to the vendors & meals dict's for 
better test coverage.
import pytest

from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta

fmt = '%Y-%m-%d %H:%M:%S'

# A dict of list of meals to be delivered
meals = {
    "results": [
        {
            "vendor_id": 1,  # Vendor 1 will be serving
            "client_id": 10,  # Client 10 on
            "datetime": "2017-01-01 13:30:00"  # January 1st, 2017 at 1:30 pm
        },
        {
            "vendor_id": 1,
            "client_id": 40,
            "datetime": "2017-01-01 14:30:00"
        },
        {
            "vendor_id": 2,
            "client_id": 20,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 3,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 3,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 3,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 3,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 3,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 4,
            "client_id": 30,
            "datetime": "2017-01-01 13:30:00"
        },
        {
            "vendor_id": 4,
            "client_id": 30,
            "datetime": "2017-01-01 13:40:00"
        },
        {
            "vendor_id": 10,
            "client_id": 40,
            "datetime": "2017-01-01 14:00:00"
        },
    ]
}

# Driver information per vendor.
vendors = {
    "results": [{
        "vendor_id": 1,
        "drivers": 1
    }, {
        "vendor_id": 2,
        "drivers": 3
    },
        {
          "vendor_id": 3,
          "drivers": 2
        },
        {
          "vendor_id": 4,
          "drivers": 2
        },
        {
          "vendor_id": 10,
          "drivers": 1
        },
        {
          "vendor_id": 13,
          "drivers": 20
        },

    ]
}


def get_avail_drivers(vendor_id):
    '''
    Function to lookup vendors and return count of drivers for given vendor id

    :param input: vendor_id int
    :outpu: count int
    '''
    count = 0
    vendor_results = vendors.get('results')

    for result in vendor_results:
        if result.get('vendor_id') == vendor_id:
            count += result.get('drivers')
    return count


def existing_orders_in_delivery_blackout_period(vendor_id, start, end):
    '''
    Function to lookup meals and return count of orders that are
    in the blackout period

    :param input: vendor_id int, start type datetime, end type datetime
    :output: count int
    '''    
    count = 0
    client_delvery_times = defaultdict(list)

    meal_results = meals.get('results')

    for result in meal_results:
        try:
          dt_obj = dt.strptime(result.get('datetime'), fmt)
        except ValueError:
          raise ValueError('Datetime not in correct format')

        if result.get('vendor_id') != vendor_id:
          continue
        
        # Check if date_time in blackout period
        if not start < dt_obj < end:
          continue

        client_id = result.get('client_id')
        delivery_dt = result.get('datetime')

        # 2 or more Deliveries with same client_id and datetime
        # will only need 1 driver
        if client_id in client_delvery_times and delivery_dt in client_delvery_times[client_id]:
          continue

        count += 1
        client_delvery_times[client_id].append(delivery_dt)
    return count


def get_total_concurrent_orders(vendor_id, date_time):
    '''
    Return total number of orders/meals for given vendor id,
    within the delivery blackout time range. 
    
    Delivery blackout range:

    start-----------date_time------end
      |-----30mins-----|---10mins---|

    :input param: vendor_id int, date_time: type datetime
    :output: int
    '''
    start_date_time = date_time - timedelta(minutes=30)
    end_date_time = date_time + timedelta(minutes=10)
    existing_orders = existing_orders_in_delivery_blackout_period(vendor_id, start_date_time, end_date_time)

    return 1 + existing_orders


def is_vendor_available(vendor_id, date_time):
    '''
    Function to check vendor Availability to deliver a meal

    :input param: vendor_id int, date_time str
    output: boolean
    '''
    vendor_id, date_time = _clean_inputs(vendor_id, date_time)

    avail_drivers = get_avail_drivers(vendor_id)
    concurrent_orders = get_total_concurrent_orders(vendor_id, date_time)

    return avail_drivers > 0 and avail_drivers >= concurrent_orders

def _clean_inputs(vendor_id, date_time):
    '''
    Utility function to handle invalid inputs and format inputs

    :param input: vendor_id int, date_time str
    :output: vendor_id int, date_time type datetime
    '''
    if not vendor_id:
      raise ValueError('Vendor ID cannot be null')

    if isinstance(vendor_id, str):
        if not vendor_id.isnumeric():
          raise ValueError('Invalid Vendor ID')
        vendor_id = int(vendor_id)

    try:
        date_time = dt.strptime(date_time, fmt)
    except ValueError:
        raise ValueError('Datetime not in correct format')

    return vendor_id, date_time

"""
Here's some tests to get you started
"""
def test_unavailable_vendor():
    assert is_vendor_available(1, "2017-01-01 14:30:00") == False
    assert is_vendor_available(40, '2020-03-01 13:00:00') == False
    assert is_vendor_available(10, '2017-01-01 14:15:00') == False
    assert is_vendor_available(1.2, "2017-01-01 14:30:00") == False

def test_available_vendor():
    assert is_vendor_available('1', "2017-01-02 14:30:00") == True
    assert is_vendor_available(1, "2017-01-01 15:10:00") == True
    assert is_vendor_available(10, '2017-01-01 14:40:00') == True
    assert is_vendor_available(13, '2017-01-01 14:40:00') == True


def test_available_vendor_dupe_client():
    '''
    Test vendor is available when serving multiple orders
    to the same client at same delivery time
    '''
    assert is_vendor_available(3, "2017-01-01 13:30:00") == True

def test_unavailable_vendor_dupe_client():
    '''
    Test vendor is available when serving multiple orders
    to the same client, at different delivery times
    '''
    assert is_vendor_available(4, "2017-01-01 13:55:00") == False

def test_invalid_inputs():
    with pytest.raises(ValueError):
      is_vendor_available(None, None)
      is_vendor_available(None, "2017-01-01 13:30:00")
      is_vendor_available(1, None)
      is_vendor_available(1, "")
      is_vendor_available('None', "2017-01-01 13:30:00")
      is_vendor_available(1, "2017/01/02 14:30:00")
      is_vendor_available(1, "2017/01/02")
      
"""
Sanity tests
"""


def test_exceptions_get_caught():
    with pytest.raises(Exception) as e_info:
        x = 1 / 0


def test_sanity():
    assert 2 + 2 == 4


pytest.main(["-x", "main.py"])

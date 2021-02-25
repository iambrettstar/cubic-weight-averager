import pytest
import requests_mock

from cwa.cli import average_cubic_weight, calculate_cubic_weight


def test_calculate_cubic_weight_empty_dict_raises_error():
    with pytest.raises(KeyError, match="'size'"):
        calculate_cubic_weight({})


def test_calculate_cubic_weight_none_raises_error():
    with pytest.raises(TypeError, match="'NoneType' object is not subscriptable"):
        calculate_cubic_weight(None)


def test_calculate_cubic_weight():
    item = {
        'size': {
            'length': 40,
            'height': 20,
            'width': 30
        },
        'weight': 5000
    }

    cubic_weight = calculate_cubic_weight(item)

    assert 6 == cubic_weight


def test_average_cubic_weight_no_objects_in_response():
    with requests_mock.Mocker() as m:
        # set mock response
        m.get(
            'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/1',
            json={
                'next': None,
                'objects': []
            }
        )

        assert 0 == average_cubic_weight()


def test_average_cubic_weight_no_items_of_category():
    with requests_mock.Mocker() as m:
        # set mock response
        m.get(
            'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/1',
            json={
                'objects': [
                    {
                        'category': 'Gadgets',
                        'title': '10 Pack Family Car Sticker Decals',
                        'weight': 120.0,
                        'size': {
                            'width': 15.0,
                            'length': 13.0,
                            'height': 1.0
                        }
                    },
                    {
                        'category': 'Batteries',
                        'title': '10 Pack Kogan CR2032 3V Button Cell Battery',
                        'weight': 60.0,
                        'size': {
                            'width': 5.8,
                            'length': 19.0,
                            'height': 0.3
                        }
                    }
                ],
                'next': None
            }
        )

        assert 0 == average_cubic_weight()


def test_average_cubic_weight_single_page():
    with requests_mock.Mocker() as m:
        # set mock response
        m.get(
            'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/1',
            json={
                'objects': [
                    {
                        'category': 'Gadgets',
                        'title': '10 Pack Family Car Sticker Decals',
                        'weight': 120.0,
                        'size': {
                            'width': 15.0,
                            'length': 13.0,
                            'height': 1.0
                        }
                    },
                    {
                        'category': 'Air Conditioners',
                        'title': 'Window Seal for Portable Air Conditioner Outlets',
                        'weight': 235.0,
                        'size': {
                            'width': 26.0,
                            'length': 26.0,
                            'height': 5.0
                        }
                    },
                    {
                        'category': 'Air Conditioners',
                        'title': 'Kogan 10,000 BTU Portable Air Conditioner (2.9KW)',
                        'weight': 26200.0,
                        'size': {
                            'width': 49.6,
                            'length': 38.7,
                            'height': 89.0
                        }
                    }
                ],
                'next': None
            }
        )

        first_item_cw = ((26.0 / 100) * (26.0 / 100) * (5.0 / 100)) * 250
        second_item_cw = ((49.6 / 100) * (38.7 / 100) * (89.0 / 100)) * 250

        expected_average = (first_item_cw + second_item_cw) / 2

        assert expected_average == average_cubic_weight()


def test_average_cubic_weight_multiple_pages():
    with requests_mock.Mocker() as m:
        # set mock response
        m.get(
            'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/1',
            json={
                'objects': [
                    {
                        'category': 'Gadgets',
                        'title': '10 Pack Family Car Sticker Decals',
                        'weight': 120.0,
                        'size': {
                            'width': 15.0,
                            'length': 13.0,
                            'height': 1.0
                        }
                    },
                    {
                        'category': 'Air Conditioners',
                        'title': 'Window Seal for Portable Air Conditioner Outlets',
                        'weight': 235.0,
                        'size': {
                            'width': 26.0,
                            'length': 26.0,
                            'height': 5.0
                        }
                    }
                ],
                'next': '/api/products/2'
            }
        )

        m.get(
            'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/2',
            json={
                'objects': [
                    {
                        'category': 'Air Conditioners',
                        'title': 'Kogan 10,000 BTU Portable Air Conditioner (2.9KW)',
                        'weight': 26200.0,
                        'size': {
                            'width': 49.6,
                            'length': 38.7,
                            'height': 89.0
                        }
                    },
                    {
                        'category': 'Cables & Adapters',
                        'title': '3 Pack Apple MFI Certified Lightning to USB Cable (3m)',
                        'weight': 90.0,
                        'size': {
                            'width': 10.0,
                            'length': 20.0,
                            'height': 3.0
                        }
                    }
                ],
                'next': None
            }
        )

        first_item_cw = ((26.0 / 100) * (26.0 / 100) * (5.0 / 100)) * 250
        second_item_cw = ((49.6 / 100) * (38.7 / 100) * (89.0 / 100)) * 250

        expected_average = (first_item_cw + second_item_cw) / 2

        assert expected_average == average_cubic_weight()

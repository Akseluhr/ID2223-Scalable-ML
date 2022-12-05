#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:30:36 2022

@author: akseluhr
"""

import os

import modal

stub = modal.Stub()


@stub.function(secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
def f():
    print(os.environ["HOPSWORKS_API_KEY"])


if __name__ == "__main__":
    with stub.run():
        f()
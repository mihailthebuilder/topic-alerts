""" Random functions """
import re


def remove_newlines(str_input):
    return re.sub(r"\n|\r", " ", str_input)
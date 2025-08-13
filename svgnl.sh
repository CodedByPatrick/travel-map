#!/bin/bash

cat "$@" | sed 's/>/>\n/g'


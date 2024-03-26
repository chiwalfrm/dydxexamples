#!/bin/sh
for s1 in ADA-USD \
APE-USD \
APT-USD \
ARB-USD \
ATOM-USD \
AVAX-USD \
BCH-USD \
BLUR-USD \
BONK-USD \
BTC-USD \
COMP-USD \
CRV-USD \
DOGE-USD \
DOT-USD \
ETC-USD \
ETH-USD \
FIL-USD \
JTO-USD \
JUP-USD \
LDO-USD \
LINK-USD \
LTC-USD \
MATIC-USD \
MKR-USD \
NEAR-USD \
OP-USD \
PEPE-USD \
SEI-USD \
SHIB-USD \
SOL-USD \
SUI-USD \
TIA-USD \
TRX-USD \
UNI-USD \
WLD-USD \
XLM-USD \
XRP-USD
do
        echo "Starting websocket for $s1..."
        python3 -u ws.py $s1 > /tmp/ws$s1.log 2>&1 &
        sleep 1
done

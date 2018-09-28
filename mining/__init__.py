"""
This file contains functions for mining.
HODL has 4 ways of mining:
pow_mining: classical mining like in Bitcoin (proofs-of-work)
pok_mining: miner stores smart contracts' data there is not only one miner, everybody who stores it becomes HODL
proof-of-keeping. It is the base for decentralized data storage.
poc_mining: miner calculates what smart contracts need (proofs-of-calcing). It is the base for dezentralized computing
in HODL.
"""
import time
import logging as log
import block
import cryptogr as cg
from block.constants import pow_total, pok_total, miningprice, block_time


# todo: replace pow with poc and change sc calculating awards


class TooLessTxsError(Exception):
    pass


class NoValidMinersError(Exception):
    pass


def pow_mining(bch, b):
    """
    Proof-of-work new block processing
    """
    lb = bch[-1]
    miners = lb.miners
    # add transaction with award sending
    txn = block.Transaction()
    outs = ['miner']   # todo
    outns = [pow_total(bch, len(bch))]
    txn.gen('mining', ['mining'], outs, outns, [len(bch), 0], sign='mining', ts=lb.timestamp + block_time)
    b.append(txn)
    b.update()
    return b


def pow_validate(bch, num):
    miners = bch[num - 1].miners
    txn = block.Transaction()
    outs = ['miner']   # todo
    outns = [pow_total(bch, len(bch))]
    txn.gen('mining', ['mining'], outs, outns, [len(bch), 0], sign='mining', ts=bch[num - 1].timestamp + block_time)
    return txn.hash == bch[num].txs[0].hash


def pok_mining(b, bch):
    """Proof-of-keeping new block processing"""
    lb = bch[-1]
    miners = lb.miners
    # add transaction with award sending
    txn = block.Transaction()
    outs = ['miner']   # todo
    outns = [pok_total(bch, len(bch))]
    txn.gen('mining', ['mining'], outs, outns, [len(bch), 0], sign='mining', ts=lb.timestamp + block_time)
    b.append(txn)
    b.update()
    return b


def pok_validate(bch, num):
    miners = bch[num - 1].miners
    txn = block.Transaction()
    outs = ['miner']   # todo
    outns = [pok_total(bch, len(bch))]
    txn.gen('mining', ['mining'], outs, outns, [len(bch), 0], sign='mining', ts=bch[num - 1].timestamp + block_time)
    return txn.hash == bch[num].txs[0].hash


def validate(bch, i=-1):
    """Checks is block mined"""
    # todo: write mining.validate()
    powv = pow_validate(bch, i)
    pokv = pok_validate(bch, i)
    log.debug(str((powv, pokv)))
    return all([powv, pokv])


def mine(bch):
    """Creates new block"""
    b = block.Block()
    b = pow_mining(bch, b)
    b = pok_mining(b, bch)
    b.prevhash = bch[-1].h
    b.update()
    return b

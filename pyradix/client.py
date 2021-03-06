import os

from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.http import HttpPostClientTransport

from pyradix.constants import DEFAULT_NODE_URL, RPC_METHOD_PREFIX


class Client:
    def __init__(self, node_url=None):
        rpc_client = RPCClient(
            JSONRPCProtocol(),
            HttpPostClientTransport(
                node_url or os.getenv("RADIX_NODE_URL") or DEFAULT_NODE_URL
            ),
        )
        self._rpc_proxy = rpc_client.get_proxy(prefix=RPC_METHOD_PREFIX)

    @property
    def network_id(self):
        return self._rpc_proxy.networkId()['networkId']

    @property
    def network_tps(self):
        return self._rpc_proxy.networkTransactionThroughput()['tps']

    @property
    def network_tps_demand(self):
        return self._rpc_proxy.networkTransactionDemand()['tps']

    @property
    def native_token(self):
        return self._rpc_proxy.nativeToken()

    def get_token_info(self, token_id):
        return self._rpc_proxy.tokenInfo(token_id)

    def get_token_balances(self, address):
        return self._rpc_proxy.tokenBalances(address)['tokenBalances']

    def get_transaction(self, transaction_id):
        return self._rpc_proxy.lookupTransaction(transaction_id)

    def get_transaction_history(self, address, n=100, cursor=1):
        return self._rpc_proxy.transactionHistory(address, n, cursor)

    def get_stake_positions(self, address):
        return self._rpc_proxy.stakePositions(address)

    def get_unstaked_positions(self, address):
        return self._rpc_proxy.unstakePositions(address)

    def get_transaction_status(self, transaction_id):
        return self._rpc_proxy.statusOfTransaction(transaction_id)['status']

    def get_validator(self, validator_id):
        # TODO: should this just be address?
        return self._rpc_proxy.lookupValidator(validator_id)

    def get_validators(self, n=100, cursor=1):
        return self._rpc_proxy.validators(n, cursor)

    def transfer_tokens(self, from_, to, amount, token_id):
        return self._build_transaction(
            [
                {
                    'type': 'TokenTransfer',
                    'from': from_,
                    'to': to,
                    'amount': amount,
                    'tokenIdentifier': token_id,
                }
            ]
        )

    def stake_tokens(self, from_, validator_id, amount):
        return self._build_transaction(
            [
                {
                    'type': 'StakeTokens',
                    'from': from_,
                    'validator': validator_id,
                    'amount': amount,
                }
            ]
        )

    def unstake_tokens(self, from_, validator_id, amount):
        return self._build_transaction(
            [
                {
                    'type': 'UnstakeTokens',
                    'from': from_,
                    'validator': validator_id,
                    'amount': amount,
                }
            ]
        )

    def submit_transaction(self, public_key, blob, signature):
        return self._rpc_proxy.submitTransaction(
            dict(blob=blob), public_key, signature
        )

    def finalize_transaction(self, public_key, blob, signature):
        return self._rpc_proxy.finalizeTransaction(
            dict(blob=blob), public_key, signature
        )

    def _build_transaction(self, params):
        return self._rpc_proxy.buildTransaction(params)

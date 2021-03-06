from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pyradix.cli import main


@patch('pyradix.cli.Client')
class TestCLI:
    @pytest.fixture(autouse=True)
    def setup_case(self):
        self.runner = CliRunner()

    def test_network_id(self, Client):
        Client.return_value = MagicMock(network_id=3)
        result = self.runner.invoke(main, ['network-id'], obj={})
        assert result.exit_code == 0
        assert result.output == '3\n'

    def test_network_tps(self, Client):
        Client.return_value = MagicMock(network_tps=15000)
        result = self.runner.invoke(main, ['network-tps'], obj={})
        assert result.exit_code == 0
        assert result.output == '15000\n'

    def test_network_tps_demand(self, Client):
        Client.return_value = MagicMock(network_tps_demand=20000)
        result = self.runner.invoke(main, ['network-tps-demand'], obj={})
        assert result.exit_code == 0
        assert result.output == '20000\n'

    def test_native_token(self, Client):
        Client.return_value = MagicMock(native_token=dict(rri='xrd'))
        result = self.runner.invoke(main, ['native-token'], obj={})
        assert result.exit_code == 0
        assert result.output == "{'rri': 'xrd'}\n"

    def test_token_balances(self, Client):
        mock_client = MagicMock(
            get_token_balances=MagicMock(
                return_value=dict(rri='xrd', amount='200')
            )
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['token-balances', '--address', 'address'], obj={}
        )
        assert result.exit_code == 0
        assert result.output == "{'amount': '200', 'rri': 'xrd'}\n"
        mock_client.get_token_balances.assert_called_once_with('address')

    def test_transaction_info(self, Client):
        mock_client = MagicMock(
            get_transaction=MagicMock(
                return_value=dict(txID='tx-id', sentAt='1995-12-17T03:24:00')
            )
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['transaction-info', '--id', 'tx-id'], obj={}
        )
        assert result.exit_code == 0
        assert (
            result.output
            == "{'sentAt': '1995-12-17T03:24:00', 'txID': 'tx-id'}\n"
        )
        mock_client.get_transaction.assert_called_once_with('tx-id')

    def test_transaction_status(self, Client):
        mock_client = MagicMock(
            get_transaction_status=MagicMock(return_value='CONFIRMED')
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['transaction-status', '--id', 'tx-id'], obj={}
        )
        assert result.exit_code == 0
        assert result.output == "CONFIRMED\n"
        mock_client.get_transaction_status.assert_called_once_with('tx-id')

    def test_transaction_history(self, Client):
        mock_client = MagicMock(
            get_transaction_history=MagicMock(return_value=[1, 2, 3])
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'transaction-history',
                '--address',
                'address',
                '--n',
                '10',
                '--cursor',
                'cursor',
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == '[1, 2, 3]\n'
        mock_client.get_transaction_history.assert_called_once_with(
            'address', 10, 'cursor'
        )

    def test_stake_positions(self, Client):
        mock_client = MagicMock(
            get_stake_positions=MagicMock(return_value=[1, 2, 3])
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['stake-positions', '--address', 'address'], obj={}
        )
        assert result.exit_code == 0
        assert result.output == '[1, 2, 3]\n'
        mock_client.get_stake_positions.assert_called_once_with('address')

    def test_unstaked_positions(self, Client):
        mock_client = MagicMock(
            get_unstaked_positions=MagicMock(return_value=[1, 2, 3])
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['unstaked-positions', '--address', 'address'], obj={}
        )
        assert result.exit_code == 0
        assert result.output == '[1, 2, 3]\n'
        mock_client.get_unstaked_positions.assert_called_once_with('address')

    def test_validator_info(self, Client):
        mock_client = MagicMock(
            get_validator=MagicMock(
                return_value=dict(txID='tx-id', sentAt='1995-12-17T03:24:00')
            )
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main, ['validator-info', '--id', 'validator-id'], obj={}
        )
        assert result.exit_code == 0
        assert (
            result.output
            == "{'sentAt': '1995-12-17T03:24:00', 'txID': 'tx-id'}\n"
        )
        mock_client.get_validator.assert_called_once_with('validator-id')

    def test_validators(self, Client):
        mock_client = MagicMock(
            get_validators=MagicMock(return_value=[1, 2, 3])
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'validators',
                '--n',
                '10',
                '--cursor',
                'cursor',
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == '[1, 2, 3]\n'
        mock_client.get_validators.assert_called_once_with(10, 'cursor')

    def test_transfer_tokens(self, Client):
        mock_client = MagicMock(
            transfer_tokens=MagicMock(return_value=dict(txId='tx-id'))
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'transfer-tokens',
                '--from',
                'from-address',
                '--to',
                'to-address',
                '--amount',
                10,
                '--token-id',
                'token-id',
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == "{'txId': 'tx-id'}\n"
        mock_client.transfer_tokens.assert_called_once_with(
            'from-address', 'to-address', '10', 'token-id'
        )

    def test_stake_tokens(self, Client):
        mock_client = MagicMock(
            stake_tokens=MagicMock(return_value=dict(txId='tx-id'))
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'stake-tokens',
                '--from',
                'from-address',
                '--validator-id',
                'validator-id',
                '--amount',
                10,
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == "{'txId': 'tx-id'}\n"
        mock_client.stake_tokens.assert_called_once_with(
            'from-address',
            'validator-id',
            '10',
        )

    def test_unstake_tokens(self, Client):
        mock_client = MagicMock(
            unstake_tokens=MagicMock(return_value=dict(txId='tx-id'))
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'unstake-tokens',
                '--from',
                'from-address',
                '--validator-id',
                'validator-id',
                '--amount',
                10,
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == "{'txId': 'tx-id'}\n"
        mock_client.unstake_tokens.assert_called_once_with(
            'from-address',
            'validator-id',
            '10',
        )

    def test_submit_transaction(self, Client):
        mock_client = MagicMock(
            submit_transaction=MagicMock(return_value=dict(txId='tx-id'))
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'submit-transaction',
                '--public-key',
                'public-key',
                '--blob',
                'blob',
                '--signature',
                'signature',
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == "{'txId': 'tx-id'}\n"
        mock_client.submit_transaction.assert_called_once_with(
            'public-key',
            'blob',
            'signature',
        )

    def test_finalize_transaction(self, Client):
        mock_client = MagicMock(
            finalize_transaction=MagicMock(return_value=dict(txId='tx-id'))
        )
        Client.return_value = mock_client
        result = self.runner.invoke(
            main,
            [
                'finalize-transaction',
                '--public-key',
                'public-key',
                '--blob',
                'blob',
                '--signature',
                'signature',
            ],
            obj={},
        )
        assert result.exit_code == 0
        assert result.output == "{'txId': 'tx-id'}\n"
        mock_client.finalize_transaction.assert_called_once_with(
            'public-key',
            'blob',
            'signature',
        )

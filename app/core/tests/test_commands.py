# mock the database behavior
from unittest.mock import patch
# from numpy import true_divide
# show the possible error from psycopg2 when connecting to db
from psycopg2 import OperationalError as Psycopg2Error
# django to call the command
from django.core.management import call_command
from django.db.utils import OperationalError
# base unit test class
from django.test import SimpleTestCase


# 以下是 mock the database ===
@patch('core.management.commands.wait_for_db.Command.check')
# core.managemnt.commands.wait_for_db.Command 檔案路徑下的function
# .check 方法由BaseCommand 提供
# ===

class CommandTests(SimpleTestCase):
    """Test commands"""

    # 檢查db是否已經準備好
    def test_wait_for_db_ready(self, patched_check):
        "test waiting for db if db already ready"
        patched_check.return_value = True

        call_command('wait_for_db')
        # the mock check the default db
        patched_check.assert_called_once_with(databases=["default"])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting operational error"""
        # 建立 mock db 連線測試
        # the first two time we raise Psycopg2Error
        # then next three time
        # postgresql 有可能是根本還沒有啟動無法接受任何connections 透過（Psycopg2Error）回傳error
        # 接下來
        # postgresql 已經啟動可以接受connections 但是測試db沒啟動 所以用OperationalError 抓error
        # 接下來 在第六次回傳 True

        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
        
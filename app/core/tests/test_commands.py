#mock the database behavior
from unittest.mock import patch
from numpy import true_divide
#show the possible error from psycopg2 when connecting to db
from psycopg2 import OperationalError as Psycopg2Error
#django to call the command
from django.core.management import call_command
from django.db.utils import OperationalError
#base unit test class
from django.test import SimpleTestCase


#以下是 mock the database ===
@patch('core.managemnt.commands.wait_for_db.Command.check')
#core.managemnt.commands.wait_for_db.Command 檔案路徑下的function
#.check 方法由BaseCommand 提供
#===

class CommandTest(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        "test waiting for db if db already ready"
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=["default"])
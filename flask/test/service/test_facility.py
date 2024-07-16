import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from api.v1.models import Facility, Constraint, Qualification, Task
from api.v1.service.facilities import validate_and_create_facility_service, delete_facility_service, get_facility_service, update_facility_service, append_data_to_facility
from api.v1.validators import post_facility_schema, put_facility_schema
from api.v1.utils.error import InvalidAPIUsage


# 単体テスト


def setup_mock_session(monkeypatch, data=None):
    mock_session = MagicMock()
    if data is not None:
        mock_query = mock_session.query.return_value
        mock_query.all.return_value = data

        def mock_filter_by(**kwargs):
            facility_id = kwargs.get('facility_id')
            return MagicMock(first=lambda: next((f for f in data if f.facility_id == facility_id), None))
        mock_query.filter_by.side_effect = mock_filter_by

    mock_scope = MagicMock()
    mock_scope.return_value.__enter__.return_value = mock_session
    monkeypatch.setattr('api.v1.service.facilities.session_scope', mock_scope)
    return mock_session


# テスト用データ


facility_data = {'facility_id': 1, 'name': 'Test Facility'}
test_data = {
    'name': 'Updated Facility',
    'constraints': [{'constraint_id': 1}],
    'qualifications': [{'qualification_id': 2}],
    'tasks': [{'task_id': 3}]
}
# Fixture to mock session_scope


@pytest.fixture
def mock_session_scope():
    with patch('api.v1.service.facilities.session_scope', return_value=MagicMock()) as mock_scope:
        yield mock_scope

# Fixture to mock validate_data


@pytest.fixture
def mock_validate_data():
    with patch('api.v1.service.facilities.validate_data') as mock_validate:
        yield mock_validate

# Fixture to mock FacilitySchema


@pytest.fixture
def mock_facility_schema():
    with patch('api.v1.service.facilities.FacilitySchema') as mock_schema:
        mock_schema_instance = mock_schema.return_value
        mock_schema_instance.dump.return_value = facility_data
        yield mock_schema_instance


@pytest.fixture
def mock_append_data_to_facility():
    with patch('api.v1.service.facilities.append_data_to_facility') as mock_append:
        yield mock_append


@pytest.mark.small
def test_validate_and_create_facility_service_small(mock_session_scope, mock_validate_data, mock_facility_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_session.flush = MagicMock()

    result = validate_and_create_facility_service(facility_data)

    # validate_dataが正しく呼び出されたかを確認
    mock_validate_data.assert_called_once_with(post_facility_schema, facility_data)

    # Facilityインスタンスが正しく作成されたかを確認
    mock_session.add.assert_called_once()
    created_facility = mock_session.add.call_args[0][0]
    assert isinstance(created_facility, Facility)
    assert created_facility.name == facility_data['name']
    assert created_facility.facility_id == facility_data['facility_id']

    # session.flushが呼び出されたかを確認
    mock_session.flush.assert_called_once()

    # FacilitySchema().dumpが正しく呼び出されたかを確認
    mock_facility_schema.dump.assert_called_once_with(created_facility)

    # 戻り値が正しいかを確認
    assert result == facility_data


@pytest.mark.small
def test_delete_facility_service_small(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_facility = MagicMock(spec=Facility)

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_facility

    # テスト対象のfacility_id
    facility_id = 1

    result = delete_facility_service(facility_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが正しい引数で呼び出されたかを確認
    mock_session.delete.assert_called_once_with(mock_facility)

    # 戻り値が期待されるものであるかを確認
    assert result == mock_facility


@pytest.mark.small
def test_delete_facility_service_not_found_small(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のfacility_id
    facility_id = 1

    result = delete_facility_service(facility_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが呼び出されていないことを確認
    mock_session.delete.assert_not_called()

    # 戻り値がNoneであるかを確認
    assert result is None


@pytest.mark.small
def test_get_facility_service_small(mock_session_scope, mock_facility_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_facility = MagicMock(spec=Facility)
    facility_data = {'id': 1, 'name': 'Test Facility'}

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_facility

    # モックされたスキーマのダンプメソッドのセットアップ
    mock_facility_schema.dump.return_value = facility_data

    # テスト対象のfacility_id
    facility_id = 1

    result = get_facility_service(facility_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # FacilitySchema().dumpが正しい引数で呼び出されたかを確認
    mock_facility_schema.dump.assert_called_once_with(mock_facility)

    # 戻り値が期待されるものであるかを確認
    assert result == facility_data


@pytest.mark.small
def test_get_facility_service_not_found_small(mock_session_scope, mock_facility_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のfacility_id
    facility_id = 1

    result = get_facility_service(facility_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # FacilitySchema().dumpが呼び出されていないことを確認
    mock_facility_schema.dump.assert_not_called()

    # 戻り値がNoneであるかを確認
    assert result is None


@pytest.mark.small
def test_update_facility_service_small(mock_session_scope, mock_validate_data, mock_append_data_to_facility, mock_facility_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_facility = MagicMock(spec=Facility)
    updated_facility_data = {'id': 1, 'name': 'Updated Facility'}

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_facility

    # モックされたスキーマのダンプメソッドのセットアップ
    mock_facility_schema.dump.return_value = updated_facility_data

    # テスト対象のfacility_id
    facility_id = 1

    result = update_facility_service(facility_id, test_data)

    # validate_dataが正しく呼び出されたかを確認
    mock_validate_data.assert_called_once_with(put_facility_schema, test_data)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # facilityの更新が正しく行われたかを確認
    assert mock_facility.name == test_data['name']
    assert mock_facility.updated_at.date() == datetime.now().date()
    assert mock_facility.constraints.clear.called
    assert mock_facility.qualifications.clear.called
    assert mock_facility.tasks.clear.called

    # append_data_to_facilityが正しく呼び出されたかを確認
    mock_append_data_to_facility.assert_any_call(
        mock_session, mock_facility, test_data, Constraint, 'constraints', 'constraint_id', 'constraints', "Constraint not found")
    mock_append_data_to_facility.assert_any_call(mock_session, mock_facility, test_data, Qualification,
                                                 'qualifications', 'qualification_id', 'qualifications', "Qualification not found")
    mock_append_data_to_facility.assert_any_call(
        mock_session, mock_facility, test_data, Task, 'tasks', 'task_id', 'tasks', "Task not found")

    # session.addが呼び出されたかを確認
    mock_session.add.assert_called_once_with(mock_facility)

    # FacilitySchema().dumpが正しく呼び出されたかを確認
    mock_facility_schema.dump.assert_called_once_with(mock_facility)

    # 戻り値が期待されるものであるかを確認
    assert result == updated_facility_data


@pytest.mark.small
def test_update_facility_service_not_found_small(mock_session_scope, mock_validate_data, mock_append_data_to_facility, mock_facility_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のfacility_id
    facility_id = 1

    with pytest.raises(InvalidAPIUsage) as exc_info:
        update_facility_service(facility_id, test_data)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Facility)
    mock_query.filter_by.assert_called_once_with(facility_id=facility_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # 例外が正しく発生したかを確認
    assert exc_info.value.status_code == 404

    # append_data_to_facilityが呼び出されていないことを確認
    mock_append_data_to_facility.assert_not_called()

    # session.addが呼び出されていないことを確認
    mock_session.add.assert_not_called()

    # FacilitySchema().dumpが呼び出されていないことを確認
    mock_facility_schema.dump.assert_not_called()

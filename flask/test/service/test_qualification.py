import pytest
from unittest.mock import patch, MagicMock
from api.v1.models import Qualification
from api.v1.validators import post_qualification_schema
from api.v1.service.qualifications import get_qualification_service, add_qualification_service, delete_qualification_service

# テスト用データ
test_data = {
    'name': 'Test Qualification'
}

# Fixture to mock session_scope


@pytest.fixture
def mock_session_scope():
    with patch('api.v1.service.qualifications.session_scope', return_value=MagicMock()) as mock_scope:
        yield mock_scope

# Fixture to mock validate_data


@pytest.fixture
def mock_validate_data():
    with patch('api.v1.service.qualifications.validate_data') as mock_validate:
        yield mock_validate

# Fixture to mock QualificationSchema


@pytest.fixture
def mock_qualification_schema():
    with patch('api.v1.service.qualifications.QualificationSchema') as mock_schema:
        mock_schema_instance = mock_schema.return_value
        mock_schema_instance.dump.return_value = test_data
        yield mock_schema_instance


@pytest.mark.small
def test_get_qualification_service(mock_session_scope, mock_qualification_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_qualifications = [MagicMock(spec=Qualification), MagicMock(spec=Qualification)]

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.all.return_value = mock_qualifications

    result = get_qualification_service()

    # クエリが正しく呼び出されたかを確認
    mock_session.query.assert_called_once_with(Qualification)
    mock_query.all.assert_called_once()

    # QualificationSchema().dumpが正しく呼び出されたかを確認
    mock_qualification_schema.dump.assert_called_once_with(mock_qualifications, many=True)

    # 戻り値が期待されるものであるかを確認
    assert result == test_data


@pytest.mark.small
def test_add_qualification_service(mock_session_scope, mock_validate_data, mock_qualification_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_session.flush = MagicMock()

    result = add_qualification_service(test_data)

    # validate_dataが正しく呼び出されたかを確認
    mock_validate_data.assert_called_once_with(post_qualification_schema, test_data)

    # Qualificationインスタンスが正しく作成されたかを確認
    mock_session.add.assert_called_once()
    created_qualification = mock_session.add.call_args[0][0]
    assert isinstance(created_qualification, Qualification)
    assert created_qualification.name == test_data['name']

    # session.flushが呼び出されたかを確認
    mock_session.flush.assert_called_once()

    # QualificationSchema().dumpが正しく呼び出されたかを確認
    mock_qualification_schema.dump.assert_called_once_with(created_qualification)

    # 戻り値が正しいかを確認
    assert result == test_data


@pytest.mark.small
def test_delete_qualification_service(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_qualification = MagicMock(spec=Qualification)

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_qualification

    # テスト対象のqualification_id
    qualification_id = 1

    result = delete_qualification_service(qualification_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Qualification)
    mock_query.filter_by.assert_called_once_with(qualification_id=qualification_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが正しい引数で呼び出されたかを確認
    mock_session.delete.assert_called_once_with(mock_qualification)

    # 戻り値が期待されるものであるかを確認
    assert result == mock_qualification


@pytest.mark.small
def test_delete_qualification_service_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のqualification_id
    qualification_id = 1

    result = delete_qualification_service(qualification_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Qualification)
    mock_query.filter_by.assert_called_once_with(qualification_id=qualification_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが呼び出されていないことを確認
    mock_session.delete.assert_not_called()

    # 戻り値がNoneであるかを確認
    assert result is None

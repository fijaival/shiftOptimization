import pytest
from unittest.mock import patch, MagicMock
from api.v1.models import Constraint
from api.v1.validators import post_constraint_schema
from api.v1.service.constraints import get_constraint_service, add_constraint_service, delete_constraint_service

# テスト用データ
test_data = {
    'name': 'Test Constraint'
}

# Fixture to mock session_scope


@pytest.fixture
def mock_session_scope():
    with patch('api.v1.service.constraints.session_scope', return_value=MagicMock()) as mock_scope:
        yield mock_scope

# Fixture to mock validate_data


@pytest.fixture
def mock_validate_data():
    with patch('api.v1.service.constraints.validate_data') as mock_validate:
        yield mock_validate

# Fixture to mock FacilitySchema


@pytest.fixture
def mock_constraint_schema():
    with patch('api.v1.service.constraints.ConstraintSchema') as mock_schema:
        mock_schema_instance = mock_schema.return_value
        mock_schema_instance.dump.return_value = test_data
        yield mock_schema_instance


@pytest.mark.small
def test_get_constraint_service(mock_session_scope, mock_constraint_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_constraints = [MagicMock(spec=Constraint), MagicMock(spec=Constraint)]

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.all.return_value = mock_constraints

    result = get_constraint_service()

    # クエリが正しく呼び出されたかを確認
    mock_session.query.assert_called_once_with(Constraint)
    mock_query.all.assert_called_once()

    # ConstraintSchema().dumpが正しく呼び出されたかを確認
    mock_constraint_schema.dump.assert_called_once_with(mock_constraints, many=True)

    # 戻り値が期待されるものであるかを確認
    assert result == test_data


@pytest.mark.small
def test_add_constraint_service(mock_session_scope, mock_validate_data, mock_constraint_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_session.flush = MagicMock()

    result = add_constraint_service(test_data)

    # validate_dataが正しく呼び出されたかを確認
    mock_validate_data.assert_called_once_with(post_constraint_schema, test_data)

    # Constraintインスタンスが正しく作成されたかを確認
    mock_session.add.assert_called_once()
    created_constraint = mock_session.add.call_args[0][0]
    assert isinstance(created_constraint, Constraint)
    assert created_constraint.name == test_data['name']

    # session.flushが呼び出されたかを確認
    mock_session.flush.assert_called_once()

    # ConstraintSchema().dumpが正しく呼び出されたかを確認
    mock_constraint_schema.dump.assert_called_once_with(created_constraint)

    # 戻り値が正しいかを確認
    assert result == test_data


@pytest.mark.small
def test_delete_constraint_service(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_constraint = MagicMock(spec=Constraint)

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_constraint

    # テスト対象のconstraint_id
    constraint_id = 1

    result = delete_constraint_service(constraint_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Constraint)
    mock_query.filter_by.assert_called_once_with(constraint_id=constraint_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが正しい引数で呼び出されたかを確認
    mock_session.delete.assert_called_once_with(mock_constraint)

    # 戻り値が期待されるものであるかを確認
    assert result == mock_constraint


@pytest.mark.small
def test_delete_constraint_service_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のconstraint_id
    constraint_id = 1

    result = delete_constraint_service(constraint_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Constraint)
    mock_query.filter_by.assert_called_once_with(constraint_id=constraint_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが呼び出されていないことを確認
    mock_session.delete.assert_not_called()

    # 戻り値がNoneであるかを確認
    assert result is None

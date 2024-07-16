import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
from api.v1.models import Qualification, Constraint, Employee, Facility, EmployeeType, Dependency, EmployeeSchema
from api.v1.validators import post_employee_schema, put_employee_schema
from api.v1.service.employees import get_all_employees_service, add_employee_service, delete_employee_service, update_employee_service, has_employee_type, has_constraint, has_qualification, has_employee
from api.v1.utils.error import InvalidAPIUsage

# テスト用データ
test_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'employee_type_id': 1,
    'constraints': [{'constraint_id': 1, 'value': 'value1'}],
    'qualifications': [{'qualification_id': 1}],
    'dependencies': [1]
}

# Fixture to mock session_scope


@pytest.fixture
def mock_session_scope():
    with patch('api.v1.service.employees.session_scope', return_value=MagicMock()) as mock_scope:
        yield mock_scope

# Fixture to mock validate_data


@pytest.fixture
def mock_validate_data():
    with patch('api.v1.service.employees.validate_data') as mock_validate:
        yield mock_validate

# Fixture to mock EmployeeSchema


@pytest.fixture
def mock_employee_schema():
    with patch('api.v1.service.employees.EmployeeSchema') as mock_schema:
        mock_schema_instance = mock_schema.return_value
        mock_schema_instance.dump.return_value = test_data
        yield mock_schema_instance


@pytest.mark.small
def test_get_all_employees_service(mock_session_scope, mock_employee_schema):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_employees = [MagicMock(spec=Employee), MagicMock(spec=Employee)]

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.all.return_value = mock_employees

    result = get_all_employees_service(1)

    # クエリが正しく呼び出されたかを確認
    mock_session.query.assert_called_once_with(Employee)
    mock_query.filter_by.assert_called_once_with(facility_id=1)
    mock_query.filter_by.return_value.all.assert_called_once()

    # EmployeeSchema().dumpが正しく呼び出されたかを確認
    mock_employee_schema.dump.assert_called_once_with(mock_employees, many=True)

    # 戻り値が期待されるものであるかを確認
    assert result == test_data


@patch('api.v1.service.employees.has_employee_type')
@patch('api.v1.service.employees.has_constraint')
@patch('api.v1.service.employees.has_qualification')
@patch('api.v1.service.employees.has_employee')
@pytest.mark.small
def test_add_employee_service(mock_has_employee, mock_has_qualification, mock_has_constraint, mock_has_employee_type, mock_employee_schema, mock_validate_data, mock_session_scope):
    # モックのセットアップ
    mock_session = MagicMock()
    mock_session_scope.return_value.__enter__.return_value = mock_session

    # 入力データの準備
    facility_id = 1
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        "constraints": [],
        'employee_type_id': 2,
        'qualifications': [{'qualification_id': 1}],
        'dependencies': [3]
    }

    # モックされたオブジェクトの作成
    mock_constraint = Constraint()
    mock_constraint.constraint_id = 1
    mock_qualification = Qualification()
    mock_qualification.qualification_id = 1

    mock_session.query(Constraint).filter_by.return_value.first.return_value = mock_constraint
    mock_session.query(Qualification).filter_by.return_value.first.return_value = mock_qualification

    # テスト対象関数の呼び出し
    result = add_employee_service(facility_id, data)

    # 検証
    mock_validate_data.assert_called_once_with(post_employee_schema, data)
    mock_has_employee_type.assert_called_once_with(data['employee_type_id'], mock_session)
    mock_has_qualification.assert_called_once_with(facility_id, data['qualifications'], mock_session)
    mock_has_employee.assert_called_once_with(facility_id, data['dependencies'], mock_session)

    # 新しいEmployeeオブジェクトの生成と属性の検証
    assert mock_session.add.call_count == 1
    new_employee = mock_session.add.call_args[0][0]
    assert new_employee.first_name == 'John'
    assert new_employee.last_name == 'Doe'
    assert new_employee.employee_type_id == 2
    assert new_employee.facility_id == facility_id

    # Qualificationsの検証
    assert len(new_employee.qualifications) == 1
    assert new_employee.qualifications[0] == mock_qualification

    # Dependenciesの検証
    assert len(new_employee.dependencies) == 1
    assert new_employee.dependencies[0].dependent_employee_id == 3

    # EmployeeSchemaのダンプの検証
    assert result == mock_employee_schema.dump.return_value
    mock_employee_schema.dump.assert_called_once_with(new_employee)


@pytest.mark.small
def test_delete_employee_service(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_employee = MagicMock(spec=Employee)

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_employee

    # テスト対象のemployee_id
    employee_id = 1

    result = delete_employee_service(employee_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Employee)
    mock_query.filter_by.assert_called_once_with(employee_id=employee_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが正しい引数で呼び出されたかを確認
    mock_session.delete.assert_called_once_with(mock_employee)

    # 戻り値が期待されるものであるかを確認
    assert result == mock_employee


@pytest.mark.small
def test_delete_employee_service_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のemployee_id
    employee_id = 1

    result = delete_employee_service(employee_id)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(Employee)
    mock_query.filter_by.assert_called_once_with(employee_id=employee_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # session.deleteが呼び出されていないことを確認
    mock_session.delete.assert_not_called()

    # 戻り値がNoneであるかを確認
    assert result is None


@pytest.mark.small
def test_update_employee_service_success(mock_session_scope, mock_validate_data, mock_employee_schema):
    session = mock_session_scope.return_value.__enter__.return_value
    employee = MagicMock()
    session.query.return_value.filter_by.return_value.first.return_value = employee

    with patch('api.v1.service.employees.has_employee_type'), \
            patch('api.v1.service.employees.has_constraint'), \
            patch('api.v1.service.employees.has_qualification'), \
            patch('api.v1.service.employees.has_employee'), \
            patch('api.v1.models.Constraint'), \
            patch('api.v1.models.Qualification'), \
            patch('api.v1.models.Dependency'):

        result = update_employee_service(1, 1, test_data)

        assert employee.first_name == test_data['first_name']
        assert employee.last_name == test_data['last_name']
        assert employee.employee_type_id == test_data['employee_type_id']
        assert mock_employee_schema.dump.call_count == 1
        assert result == test_data


@pytest.mark.small
def test_update_employee_service_employee_not_found(mock_session_scope, mock_validate_data):
    session = mock_session_scope.return_value.__enter__.return_value
    session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(InvalidAPIUsage) as exc_info:
        update_employee_service(1, 1, test_data)

    assert exc_info.value.status_code == 404
    # assert str(exc_info.value) == "Employee not found"
    assert mock_validate_data.call_count == 1


@pytest.mark.small
def test_has_employee_type(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_employee_type = MagicMock(spec=EmployeeType)

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_employee_type

    # テスト対象のemployee_type_id
    employee_type_id = 1

    has_employee_type(employee_type_id, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(EmployeeType)
    mock_query.filter_by.assert_called_once_with(employee_type_id=employee_type_id)
    mock_query.filter_by.return_value.first.assert_called_once()


@pytest.mark.small
def test_has_employee_type_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # テスト対象のemployee_type_id
    employee_type_id = 1

    with pytest.raises(InvalidAPIUsage) as exc_info:
        has_employee_type(employee_type_id, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query.assert_called_once_with(EmployeeType)
    mock_query.filter_by.assert_called_once_with(employee_type_id=employee_type_id)
    mock_query.filter_by.return_value.first.assert_called_once()

    # 例外が正しく発生したかを確認
    assert exc_info.value.status_code == 404
    # assert str(exc_info.value) == "Employee type not found"


@pytest.mark.small
def test_has_constraint():
    # モックオブジェクトの作成
    mock_session = MagicMock()
    mock_facility = MagicMock(spec=Facility)
    mock_constraint = MagicMock(spec=Constraint)

    # モックオブジェクトに属性を追加
    mock_facility.constraints = [mock_constraint]
    mock_constraint.constraint_id = 1

    # モックされたクエリのセットアップ
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [mock_facility, mock_constraint]

    # テスト対象のfacility_idおよびconstraints
    facility_id = 1
    constraints = [{'constraint_id': 1}]

    # テスト関数の呼び出し
    has_constraint(facility_id, constraints, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query(Facility).filter_by.assert_any_call(facility_id=facility_id)
    mock_session.query(Constraint).filter_by.assert_any_call(constraint_id=1)


@pytest.mark.small
def test_has_constraint_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_facility = MagicMock(spec=Facility)
    mock_facility.constraints = []

    # モックされたクエリのセットアップ
    mock_query_facility = mock_session.query(Facility).filter_by.return_value
    mock_query_facility.first.return_value = mock_facility
    mock_query_constraint = mock_session.query(Constraint).filter_by.return_value
    mock_query_constraint.first.return_value = None

    # テスト対象のfacility_idおよびconstraints
    facility_id = 1
    constraints = [{'constraint_id': 1}]

    with pytest.raises(InvalidAPIUsage) as exc_info:
        has_constraint(facility_id, constraints, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    calls = [call(facility_id=facility_id), call().first(), call(constraint_id=1), call().first()]
    mock_session.query(Facility).filter_by.assert_has_calls(calls[:2])
    mock_session.query(Constraint).filter_by.assert_has_calls(calls[2:])

    # 例外が正しく発生したかを確認
    assert exc_info.value.status_code == 404


@pytest.mark.small
def test_has_qualification(mock_session_scope):
    # モックオブジェクトの作成
    mock_session = MagicMock()
    mock_facility = MagicMock(spec=Facility)
    mock_qualification = MagicMock(spec=Qualification)

    # モックオブジェクトに属性を追加
    mock_facility.qualifications = [mock_qualification]
    mock_qualification.qualification_id = 1

    # モックされたクエリのセットアップ
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [mock_facility, mock_qualification]

    # テスト対象のfacility_idおよびqualifications
    facility_id = 1
    qualifications = [{'qualification_id': 1}]

    # テスト関数の呼び出し
    has_qualification(facility_id, qualifications, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query(Facility).filter_by.assert_any_call(facility_id=facility_id)
    mock_session.query(Qualification).filter_by.assert_any_call(qualification_id=1)


@pytest.mark.small
def test_has_qualification_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_facility = MagicMock(spec=Facility)
    mock_facility.qualifications = []

    # モックされたクエリのセットアップ
    mock_query_facility = mock_session.query(Facility).filter_by.return_value
    mock_query_facility.first.return_value = mock_facility
    mock_query_qualification = mock_session.query(Qualification).filter_by.return_value
    mock_query_qualification.first.return_value = None

    # テスト対象のfacility_idおよびqualifications
    facility_id = 1
    qualifications = [{'qualification_id': 1}]

    with pytest.raises(InvalidAPIUsage) as exc_info:
        has_qualification(facility_id, qualifications, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    calls = [call(facility_id=facility_id), call().first(), call(qualification_id=1), call().first()]
    mock_session.query(Facility).filter_by.assert_has_calls(calls[:2])
    mock_session.query(Qualification).filter_by.assert_has_calls(calls[2:])

    # 例外が正しく発生したかを確認
    assert exc_info.value.status_code == 404


@pytest.mark.small
def test_has_employee(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value
    mock_employee = MagicMock(spec=Employee)

    # モックされたクエリのセットアップ
    mock_query_employee = mock_session.query(Employee).filter_by.return_value
    mock_query_employee.first.return_value = mock_employee

    # テスト対象のfacility_idおよびdependencies
    facility_id = 1
    dependencies = [1]

    has_employee(facility_id, dependencies, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query(Employee).filter_by.assert_called_once_with(employee_id=1, facility_id=facility_id)
    mock_query_employee.first.assert_called_once()


@pytest.mark.small
def test_has_employee_not_found(mock_session_scope):
    mock_session = mock_session_scope.return_value.__enter__.return_value

    # モックされたクエリのセットアップ
    mock_query_employee = mock_session.query(Employee).filter_by.return_value
    mock_query_employee.first.return_value = None

    # テスト対象のfacility_idおよびdependencies
    facility_id = 1
    dependencies = [1]

    with pytest.raises(InvalidAPIUsage) as exc_info:
        has_employee(facility_id, dependencies, mock_session)

    # クエリが正しい引数で呼び出されたかを確認
    mock_session.query(Employee).filter_by.assert_called_once_with(employee_id=1, facility_id=facility_id)
    mock_query_employee.first.assert_called_once()

    # 例外が正しく発生したかを確認
    assert exc_info.value.status_code == 404
    # assert str(exc_info.value) == "dependency not found"

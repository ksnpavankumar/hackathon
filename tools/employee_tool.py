from langchain_core.tools import tool

from tools.employee_mcp_client import (
    run_employee_mcp
)


@tool
def get_employee(
    employee_identifier: str
) -> dict:
    """
    Find an employee by employee ID,
    email address, or full name.
    """

    return run_employee_mcp(
        "get_employee",
        {
            "employee_identifier":
                employee_identifier
        }
    )


@tool
def get_employee_leave_balance(
    employee_id: str
) -> dict:
    """
    Retrieve the leave balance for an employee.
    """

    return run_employee_mcp(
        "get_employee_leave_balance",
        {
            "employee_id": employee_id
        }
    )


@tool
def get_employee_projects(
    employee_id: str
) -> dict:
    """
    Retrieve projects assigned to an employee.
    """

    return run_employee_mcp(
        "get_employee_projects",
        {
            "employee_id": employee_id
        }
    )

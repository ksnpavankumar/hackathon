import os
import httpx

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

EMPLOYEE_API_BASE_URL = os.getenv(
    "EMPLOYEE_API_BASE_URL",
    "http://localhost:3000"
)

mcp = FastMCP("Employee Directory MCP")


# ============================================================
# EMPLOYEE LOOKUP
# ============================================================

@mcp.tool
def get_employee(employee_identifier: str) -> dict:
    """
    Find an employee by employee ID, email, or name.

    Example:
        EMP001
        alice.brown@bank.com
        Alice Brown
    """

    try:
        response = httpx.get(
            f"{EMPLOYEE_API_BASE_URL}/employees",
            timeout=10.0
        )

        response.raise_for_status()

        employees = response.json()

        identifier = employee_identifier.strip().lower()

        for employee in employees:

            employee_id = str(
                employee.get("employeeId", "")
            ).lower()

            email = str(
                employee.get("email", "")
            ).lower()

            full_name = str(
                employee.get("fullName", "")
            ).lower()

            if (
                identifier == employee_id
                or identifier == email
                or identifier == full_name
            ):
                return {
                    "status": "success",
                    "employee": employee
                }

        return {
            "status": "not_found",
            "message": (
                f"Employee '{employee_identifier}' "
                "was not found."
            )
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc)
        }


# ============================================================
# EMPLOYEE LEAVE
# ============================================================

@mcp.tool
def get_employee_leave_balance(
    employee_id: str
) -> dict:
    """
    Retrieve leave balance for an employee.
    """

    try:

        response = httpx.get(
            f"{EMPLOYEE_API_BASE_URL}/employeeLeaveBalances",
            timeout=10.0
        )

        response.raise_for_status()

        records = response.json()

        employee_id = employee_id.strip().lower()

        for record in records:

            record_employee_id = str(
                record.get("employeeId", "")
            ).lower()

            if record_employee_id == employee_id:

                return {
                    "status": "success",
                    "leaveBalance": record
                }

        return {
            "status": "not_found",
            "message": (
                f"No leave information found "
                f"for employee '{employee_id}'."
            )
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc)
        }


# ============================================================
# EMPLOYEE PROJECTS
# ============================================================

@mcp.tool
def get_employee_projects(
    employee_id: str
) -> dict:
    """
    Retrieve project assignments for an employee.
    """

    try:

        response = httpx.get(
            f"{EMPLOYEE_API_BASE_URL}/employeeProjectInformation",
            timeout=10.0
        )

        response.raise_for_status()

        records = response.json()

        employee_id = employee_id.strip().lower()

        for record in records:

            record_employee_id = str(
                record.get("employeeId", "")
            ).lower()

            if record_employee_id == employee_id:

                return {
                    "status": "success",
                    "projects": record
                }

        return {
            "status": "not_found",
            "message": (
                f"No project information found "
                f"for employee '{employee_id}'."
            )
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc)
        }


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Employee MCP Server")
    print("=" * 60)
    print(
        f"JSON Server: {EMPLOYEE_API_BASE_URL}"
    )
    print("=" * 60)

    mcp.run(
        transport="streamable-http"
    )
import asyncio
import argparse
import sys

from pydantic import ValidationError

from ..db.unitofwork import UnitOfWork
from ..admin.schemas import AdminCreateSchema
from ..admin.service import AdminAuthService


async def main(argv=sys.argv):
    description = """
    This script is used to create an admin user.
    """

    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument(
        "-u",
        "--username",
        help="Username for the admin user",
        required=True,
    )

    parser.add_argument(
        "-p",
        "--password",
        help="Password for the admin user",
        required=True,
    )

    parser.add_argument(
        "-p_conf",
        "--password-confirm",
        help="Confirm password for the admin user",
        required=True,
    )

    args = parser.parse_args(argv[1:])

    try:
        data = AdminCreateSchema(
            username=args.username,
            password=args.password,
            password_confirm=args.password_confirm,
        )
    except ValidationError as e:
        parser.error(e)
        return

    create_data = await AdminAuthService(UnitOfWork()).create_admin(data)
    if not create_data.created:
        parser.error(create_data.error)
        return
    print("Admin user created successfully!")

if __name__ == "__main__":
    asyncio.run(main())

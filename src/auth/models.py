from sqlalchemy import MetaData , Boolean, Table, Column , Integer , String , TIMESTAMP , ForeignKey
import datetime 

metadata = MetaData()
 

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),  
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("fa_surname", String),
    Column("phone_number", String, nullable=False),
    Column("snils", Integer, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("email" ,String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)
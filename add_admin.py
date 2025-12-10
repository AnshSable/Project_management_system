import pandas as pd
from passlib.context import CryptContext
import os

ADMIN_CREDS_FILE = 'data/admin_credentials.xlsx'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = input("Admin username: ").strip()
password = input("Admin password: ").strip()

hashed_password = pwd_context.hash(password)

if os.path.exists(ADMIN_CREDS_FILE):
    df = pd.read_excel(ADMIN_CREDS_FILE)
else:
    df = pd.DataFrame(columns=['username', 'password'])

if username in df['username'].values:
    df.loc[df['username'] == username, 'password'] = hashed_password
else:
    df = pd.concat([df, pd.DataFrame([{'username': username, 'password': hashed_password}])], ignore_index=True)

df.to_excel(ADMIN_CREDS_FILE, index=False)
print(f"Admin '{username}' added/updated successfully.")
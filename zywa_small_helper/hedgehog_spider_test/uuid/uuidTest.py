import uuid


if __name__ == '__main__':
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    print(mac)

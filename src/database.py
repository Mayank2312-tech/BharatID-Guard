import sqlite3


DB_NAME = "bharatid_guard.db"


def create_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_type TEXT NOT NULL,
            document_number TEXT UNIQUE NOT NULL,
            holder_name TEXT,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_sample_data():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    sample_documents = [
        (
            "PAN Card",
            "ABCDE1234F",
            "Demo Person",
            "VALID"
        ),
        (
            "PAN Card",
            "AAAAA1111A",
            "Expired Person",
            "EXPIRED"
        ),
        (
            "PAN Card",
            "BBBBB2222B",
            "Flagged Person",
            "FLAGGED"
        ),
        (
            "Indian Passport",
            "A1234567",
            "Demo Passport Holder",
            "VALID"
        ),
        (
            "Indian Passport",
            "B7654321",
            "Expired Passport Holder",
            "EXPIRED"
        )
    ]

    for document in sample_documents:

        try:

            cursor.execute("""
                INSERT INTO documents
                (document_type, document_number, holder_name, status)
                VALUES (?, ?, ?, ?)
            """, document)

        except sqlite3.IntegrityError:

            pass

    connection.commit()
    connection.close()


def check_document(document_number):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT document_type,
               document_number,
               holder_name,
               status
        FROM documents
        WHERE document_number = ?
    """, (document_number,))

    result = cursor.fetchone()

    connection.close()

    return result
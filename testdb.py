from pymongo import MongoClient, errors

MONGO_URI = (
    "mongodb+srv://shaikhshifu15:3HUDrVwTMzirR1mx"
    "@portfolio.qnfwjlx.mongodb.net/portfolio_db"
    "?retryWrites=true&w=majority&appName=portfolio"
)

def test_connection():
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=True  # <-- skips cert validation
        )
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully (certificate check skipped)!")
    except errors.ServerSelectionTimeoutError as err:
        print("❌ Failed to connect to MongoDB:")
        print(err)

if __name__ == "__main__":
    test_connection()

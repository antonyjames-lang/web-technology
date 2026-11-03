import os
import sys
import logging
import mongoengine
import pymongo

logger = logging.getLogger(__name__)

_CONNECTED = False

def init_mongo():
    global _CONNECTED
    if _CONNECTED:
        return

    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/yojana_mitra")
    db_name = os.getenv("MONGODB_DB", "yojana_mitra")

    # Try connecting to real MongoDB first
    try:
        # Quick ping to check if server is reachable within 5 seconds
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        mongoengine.connect(db=db_name, host=uri, alias="default")
        logger.info("Connected to live MongoDB database '%s'.", db_name)
        print(f"[Yojana Mitra] Connected to live MongoDB database '{db_name}'.")
        _CONNECTED = True
        return
    except Exception as exc:
        error_type = type(exc).__name__
        logger.warning("Could not connect to configured MongoDB (%s). Falling back to mongomock.", error_type)
        print(f"[Yojana Mitra] Configured MongoDB is not reachable ({error_type}). Falling back to in-memory mongomock for development.")

    # Fallback to mongomock for instant local development/testing without requiring mongod daemon
    try:
        import mongomock
        mongoengine.connect(
            db=db_name,
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
            alias="default"
        )
        logger.info("Connected to mongomock in-memory database.")
        print("[Yojana Mitra] Active in-memory mongomock database ready.")
        _CONNECTED = True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        print(f"[Yojana Mitra Error] Failed to connect: {e}", file=sys.stderr)

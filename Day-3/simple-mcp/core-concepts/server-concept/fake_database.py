class Database:
    """A fake database class for demonstration purposes"""
    
    def __init__(self):
        self.connected = False
        
    @classmethod
    async def connect(cls) -> 'Database':
        """Simulate database connection"""
        db = cls()
        db.connected = True
        print("Connected to fake database")
        return db
    
    async def disconnect(self) -> None:
        """Simulate database disconnection"""
        self.connected = False
        print("Disconnected from fake database")
    
    def query(self) -> str:
        """Simulate a database query"""
        if not self.connected:
            raise RuntimeError("Database not connected")
        return "Fake query result" 
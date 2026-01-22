"""
Lightweight Supabase client wrapper using postgrest
This avoids the pyroaring dependency issue in the full supabase client
"""

from postgrest import SyncPostgrestClient
from typing import Any

class SupabaseClient:
    """Simple wrapper to make postgrest work like supabase client"""
    
    def __init__(self, url: str, key: str):
        self.url = url.rstrip('/')
        self.key = key
        self.rest_url = f"{self.url}/rest/v1"
        
    def table(self, table_name: str):
        """Return a table interface"""
        return TableInterface(self.rest_url, table_name, self.key)

class TableInterface:
    """Table operations interface"""
    
    def __init__(self, base_url: str, table_name: str, key: str):
        self.client = SyncPostgrestClient(base_url, headers={
            "apikey": key,
            "Authorization": f"Bearer {key}"
        })
        self.table_name = table_name
        self._query = None
        
    def select(self, columns: str = "*"):
        """Select columns"""
        self._query = self.client.from_(self.table_name).select(columns)
        return self
        
    def insert(self, data: dict):
        """Insert data"""
        self._query = self.client.from_(self.table_name).insert(data)
        return self
        
    def update(self, data: dict):
        """Update data"""
        self._query = self.client.from_(self.table_name).update(data)
        return self
        
    def delete(self):
        """Delete data"""
        self._query = self.client.from_(self.table_name).delete()
        return self
        
    def eq(self, column: str, value: Any):
        """Add equality filter"""
        if self._query:
            self._query = self._query.eq(column, value)
        return self
        
    def order(self, column: str, desc: bool = False):
        """Add ordering"""
        if self._query:
            self._query = self._query.order(column, desc=desc)
        return self
        
    def execute(self):
        """Execute the query"""
        if self._query:
            result = self._query.execute()
            return result
        return None

def create_client(url: str, key: str) -> SupabaseClient:
    """Create a supabase client"""
    return SupabaseClient(url, key)

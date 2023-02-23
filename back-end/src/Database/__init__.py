"""
    Gestion de la base de données
    Table disponible:
        - tokenTable
        - userTable
        - commentTable
        - planteTable
        - conversationTable
        - privateMessageTable
"""
from supabase import create_client, Client


API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV6eXFma3ZleWVpbmdrb3h5Z2htIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3NzA4NzA4NSwiZXhwIjoxOTkyNjYzMDg1fQ.7Vs0ng29VYKE0ttjW1t3SXL4hS_lJbd63gCJsoUrxKg"
URL = "https://ezyqfkveyeingkoxyghm.supabase.co"



db: Client = create_client(URL, API_KEY)
# response= db.table('userType').select("*").or_("name", "eq", "Admin").or_("name", "eq", "Botaniste").execute().data
# print(response.data)
# input()

from Database.Tables import *


from Database.Token import TokenTable
from Database.User import UserTable
from Database.Comment import CommentTable
from Database.Plante import PlanteTable
from Database.Conversation import ConversationTable
from Database.PrivateMessage import PrivateMessageTable

tokenTable: TokenTable = TokenTable(db)
userTable = UserTable(db, tokenTable)
commentTable = CommentTable(db, userTable)
planteTable = PlanteTable(db, userTable, commentTable)
conversationTable = ConversationTable(db, userTable)
privateMessageTable = PrivateMessageTable(db, userTable)

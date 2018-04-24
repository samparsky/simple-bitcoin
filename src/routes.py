from japronto import Application
from src.controller import TransactionController, AddressController

app = Application()
app.router.add_route('/transaction', TransactionController().get, method="GET")
app.router.add_route('/address', AddressController().get, method="GET")
app.router.add_route('/address', AddressController().delete, method="DELETE")
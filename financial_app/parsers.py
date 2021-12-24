from . import api
from flask_restx.fields import date_from_iso8601

#Transaction ID parser
transaction_id_parser = api.parser()
transaction_id_parser.add_argument('transaction_id', type=int, default='1', required=True)

#User ID parser
user_id_parser = api.parser()
user_id_parser.add_argument('user_id', type=int, default='1', required=True)

#Sorting preference parser
sorting_parser = api.parser()
sorting_parser.add_argument('sort', type=str, choices=("By date", "By amount"))

#Filter preference parser
filter_parser = api.parser()
filter_parser.add_argument('filter', type=str, choices=("By income", "By outcome"))

#POST transaction parser
transaction_parser = api.parser()
transaction_parser.add_argument('user_id', type=int, required=True)
transaction_parser.add_argument('tr_amount', type=float, required=True)
transaction_parser.add_argument('tr_date', type=date_from_iso8601)

#POST user parser
user_parser = api.parser()
user_parser.add_argument('email', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)
user_parser.add_argument('first_name', type=str, required=True)
user_parser.add_argument('last_name', type=str, required=True)

#PUT transaction parser
transaction_update_parser = api.parser()
transaction_update_parser.add_argument('user_id', type=int)
transaction_update_parser.add_argument('tr_amount', type=float)
transaction_update_parser.add_argument('tr_date', type=date_from_iso8601)

#PUT user parser
user_update_parser = api.parser()
user_update_parser.add_argument('email', type=str)
user_update_parser.add_argument('password', type=str)
user_update_parser.add_argument('first_name', type=str)
user_update_parser.add_argument('last_name', type=str)

#Transaction dates parser
transaction_date_parser = api.parser()
transaction_date_parser.add_argument('start_date', type=date_from_iso8601, required=True)
transaction_date_parser.add_argument('end_date', type=date_from_iso8601, required=True)

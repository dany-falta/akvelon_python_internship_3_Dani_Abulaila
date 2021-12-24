from flask import Flask
from flask_restx import Api, Resource, Namespace
from financial_app import api, db
from financial_app import models
from financial_app import parsers as pr
from datetime import date
from sqlalchemy import and_, desc

api = Namespace('Finance', description='Financial operations')

@api.route('/view_transactions')
class ViewTransactions(Resource):
    transaction_schema = models.TransactionSchema(exclude=["user"])

    @api.doc(id= 'get_transaction', description="Query all transactions")
    def get(self):
        """ Return information on all transactions """

        transactions = db.session.query(models.Transaction).all()
        return self.transaction_schema.dump(transactions, many=True), 200

@api.route('/view_transactions_by_id')
class ViewTransactionByID(Resource):
    transaction_schema = models.TransactionSchema()

    @api.doc(id= 'get_transaction_by_id',  description="Query transaction by ID")
    @api.expect(pr.transaction_id_parser)
    def get(self, transaction_id_parser=pr.transaction_id_parser):
        """ Return information on a single transaction """

        arg = transaction_id_parser.parse_args()
        transaction_id = arg['transaction_id']

        transaction = db.session.query(models.Transaction).filter_by(transaction_id=transaction_id).first()

        if not transaction:
            return 'Transaction not found.', 404
        return self.transaction_schema.dump(transaction), 200

@api.route('/create_transaction')
class CreateTransaction(Resource):
    transaction_schema = models.TransactionSchema()

    @api.doc(id= 'create_transaction', description="Create a new transaction")
    @api.expect(pr.transaction_parser)
    def post(self, transaction_parser=pr.transaction_parser):
       """ Create a new transaction """

       data = transaction_parser.parse_args()
       user_id = data['user_id']
       tr_amount = data['tr_amount']
       tr_date = data['tr_date']

       user = db.session.query(models.User).filter_by(user_id=user_id).first()

       if not user:
           return 'User not found.', 404
       elif tr_amount == 0:
           return 'The transaction amount has to be a non-zero number.', 422
       elif tr_date and tr_date > date.today():
           return 'Transaction date can\'t be in the future.', 422
       else:
           transaction = models.Transaction(user_id=user_id, tr_amount=tr_amount, tr_date=tr_date)
           db.session.add(transaction)
           db.session.commit()
           return self.transaction_schema.dump(transaction), 200

@api.route('/update_transaction')
class UpdateTransaction(Resource):
    transaction_schema = models.TransactionSchema()

    @api.doc(id= 'update_transaction', description="Update information on an existing transaction")
    @api.expect(pr.transaction_id_parser, pr.transaction_update_parser)
    def put(self, transaction_id_parser=pr.transaction_id_parser, transaction_update_parser=pr.transaction_update_parser):
       """ Update information on an existing transaction """

       arg = transaction_id_parser.parse_args()
       transaction_id = arg['transaction_id']
       transaction = db.session.query(models.Transaction).filter_by(transaction_id=transaction_id).first()
       if not transaction:
           return 'Transaction not found.', 404

       data = transaction_update_parser.parse_args()
       user_id = data['user_id']
       tr_amount = data['tr_amount']
       tr_date = data['tr_date']

       user = db.session.query(models.User).filter_by(user_id=user_id).first()

       if not user and user_id:
           return 'User not found.', 404
       elif not tr_amount is None and tr_amount == 0:
           return 'The transaction amount has to be a non-zero number.', 422
       elif not tr_date is None and tr_date > date.today():
           return 'Transaction date can\'t be in the future.', 422
       else:
           if user_id:
               transaction.user_id = user_id
           if tr_amount:
               transaction.tr_amount = tr_amount
           if tr_date:
               transaction.tr_date = tr_date
           db.session.commit()
           return self.transaction_schema.dump(transaction), 200

@api.route('/delete_transaction')
class DeleteTransaction(Resource):
    @api.doc(id= 'delete_transaction', description="Delete an existing transaction")
    @api.expect(pr.transaction_id_parser)
    def delete(self, transaction_id_parser=pr.transaction_id_parser):
        """ Delete an existing transaction """

        arg = transaction_id_parser.parse_args()
        transaction_id = arg['transaction_id']
        transaction = db.session.query(models.Transaction).filter_by(transaction_id=transaction_id).first()
        if not transaction:
            return 'Transaction not found.', 404

        db.session.delete(transaction)
        db.session.commit()
        return 'Transaction deleted successfully', 200


@api.route('/view_user_transactions')
class ViewTransactionByID(Resource):
    transaction_schema = models.TransactionSchema()

    @api.doc(id= 'view_user_transactions', description="Query transactions by a user ID")
    @api.expect(pr.user_id_parser, pr.sorting_parser, pr.filter_parser)
    def get(self, user_id_parser=pr.user_id_parser, sorting_parser=pr.sorting_parser, filter_parser=pr.filter_parser):
        """ Return all transactions of a single user """

        arg = user_id_parser.parse_args()
        user_id = arg['user_id']

        sort = sorting_parser.parse_args()
        filter = filter_parser.parse_args()

        user = db.session.query(models.User).filter_by(user_id=user_id).first()
        if not user:
            return 'User not found.', 404

        if sort['sort'] == "By date":
            transactions = db.session.query(models.Transaction).filter_by(user_id=user_id).order_by(desc(models.Transaction.tr_date))
        elif sort['sort'] == "By amount":
            transactions = db.session.query(models.Transaction).filter_by(user_id=user_id).order_by((models.Transaction.tr_amount))
        else:
            transactions = db.session.query(models.Transaction).filter_by(user_id=user_id)

        if not transactions:
            return 'Transactions not found.', 404
        if filter['filter'] == "By income":
            transactions = transactions.filter(models.Transaction.tr_amount > 0)
        elif filter['filter'] == "By outcome":
            transactions = transactions.filter(models.Transaction.tr_amount < 0)
        return self.transaction_schema.dump(transactions, many=True), 200


@api.route('/view_user_transactions_by_date')
class ViewTransactionByID(Resource):
    transaction_schema = models.TransactionSchema()

    @api.doc(id= 'view_user_transactions_by_date', description="Query transactions by a user ID grouped by date")
    @api.expect(pr.user_id_parser, pr.transaction_date_parser)
    def get(self, user_id_parser=pr.user_id_parser, transaction_date_parser=pr.transaction_date_parser):
        """ Return sum of transactions of a single user by date """

        arg = user_id_parser.parse_args()
        user_id = arg['user_id']
        dates = transaction_date_parser.parse_args()
        start_date = dates['start_date']
        end_date = dates['end_date']
        sum = 0.0

        user = db.session.query(models.User).filter_by(user_id=user_id).first()
        if not user:
            return 'User not found.', 404

        transactions = db.session.query(models.Transaction).filter(and_(models.Transaction.tr_date \
                        >= start_date, models.Transaction.tr_date <= end_date)).filter_by(user_id=\

                        user_id).all()
        if not transactions:
            return 'Transactions not found.', 404
        for tr_amount in transactions:
            sum += tr_amount.tr_amount
        return {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), "sum": sum}, 200

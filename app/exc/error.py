class CategorySearchError(Exception):
    pass


class DateError(Exception):
    pass


class TransactionCreateError(Exception):
    pass


class GetTransactionError(Exception):
    pass


class GetCategoryForbidden(Exception):
    pass


class GetSharedCategoryForbidden(Exception):
    pass

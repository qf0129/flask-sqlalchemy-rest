from flask import request, jsonify, current_app
from flask.views import MethodView
import datetime
from dateutil.parser import parse
from sqlalchemy.sql import sqltypes


class RestModel(MethodView):

    def __init__(self, db, model, ignore_columns=[], max_page_size=100):
        self.db = db
        self.model = model
        self.ignore_columns = ignore_columns
        self.max_page_size = max_page_size

    def get(self, id=None):
        if id is None:
            return self.query_all()
        else:
            obj = self.model.query.get(id)
            if obj:
                return self._resp(data=self._to_dict(obj))
            return self._resp(code=404, msg='obj not found')

    def delete(self, id):
        obj = self.model.query.get(id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
        return self._resp()

    def post(self):
        if request.is_json:
            try:
                obj = self.model()
                obj = self._update_model_from_dict(obj, request.json)
                self.db.session.add(obj)
                self.db.session.commit()
                return self._resp(data={"id": obj.id})
            except Exception as e:
                current_app.logger.warning(str(e))
                return self._resp(code=400, msg='invalid data')
        return self._resp(code=400, msg='invalid json')

    def put(self, id):
        if request.is_json:
            obj = self.model.query.get(id)
            if obj:
                try:
                    obj = self._update_model_from_dict(obj, request.json)
                    self.db.session.commit()
                    return self._resp(data={"id": obj.id})
                except Exception as e:
                    current_app.logger.warning(str(e))
                    return self._resp(code=400, msg='invalid data')
            else:
                return self._resp(code=404, msg='obj not found')
        return self._resp(code=400, msg='invalid json')

    def query_all(self):
        page = request.args.get('_page', 1)
        page = int(page) if isinstance(page, int) or page.isdigit() else 1
        page_size = request.args.get('_page_size', 10)
        page_size = int(page_size) if isinstance(page, int) or page_size.isdigit() else 10
        if self.max_page_size is not None and self.max_page_size > 0:
            page_size = page_size if page_size <= self.max_page_size else self.max_page_size
        sort = request.args.get('_sort')
        desc = request.args.get('_desc')

        query = self.model.query
        for k, v in request.args.items():
            if isinstance(k, str):
                ks = k.split(':')
                if hasattr(self.model, ks[0]):
                    col = getattr(self.model, ks[0])
                    v = self._filter_datetime(type(col.type), v)
                    if len(ks) > 1:
                        v = None if v == 'null' else v
                        if ks[1] == 'eq':
                            query = query.filter(col == v)
                        if ks[1] == 'ne':
                            query = query.filter(col != v)
                        if ks[1] == 'in':
                            query = query.filter(col.in_(v.split(',')))
                        if ks[1] == 'notin':
                            query = query.filter(col.notin_(v.split(',')))
                        if ks[1] == 'contains':
                            query = query.filter(col.contains(v))
                        if ks[1] == 'gt':
                            query = query.filter(col > v)
                        if ks[1] == 'ge':
                            query = query.filter(col >= v)
                        if ks[1] == 'lt':
                            query = query.filter(col < v)
                        if ks[1] == 'le':
                            query = query.filter(col <= v)
                    else:
                        query = query.filter(col == v)

        if sort and hasattr(self.model, sort):
            if desc and str(desc) == '1':
                query = query.order_by(getattr(self.model, sort).desc())
            else:
                query = query.order_by(getattr(self.model, sort))

        total = query.count()
        objs = query.slice((page - 1) * page_size, page * page_size).all()
        ret = {"list": [self._to_dict(o) for o in objs], "page": page, "page_size": page_size, "total": total}
        return self._resp(data=ret)

    def _to_dict(self, obj):
        ret = {}
        for column in obj.__table__.columns:
            if column.name not in self.ignore_columns:
                value = getattr(obj, column.name)
                if type(value) in [datetime.datetime, datetime.date, datetime.time]:
                    ret[column.name] = str(value)
                else:
                    ret[column.name] = value
        return ret

    def _update_model_from_dict(self, obj, data):
        if obj and data:
            for k, v in data.items():
                if hasattr(obj, k):
                    column_type = getattr(obj.__table__.columns, k).type
                    v = self._filter_datetime(type(column_type), v)
                    setattr(obj, k, v)
        return obj

    def _filter_datetime(self, type, obj):
        if obj:
            if type == sqltypes.DateTime:
                obj = parse(obj)
            if type == sqltypes.Date:
                obj = parse(obj).date()
            if type == sqltypes.Time:
                obj = parse(obj).time()
        return obj

    def _resp(self, code=200, msg="OK", data={}):
        return jsonify(code=code, msg=msg, data=data), code

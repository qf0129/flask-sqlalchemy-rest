from flask import request, jsonify, current_app
from flask.views import MethodView
from dateutil.parser import parse
from sqlalchemy.sql import sqltypes
import json


class RestModel(MethodView):

    def __init__(self, db, model, ignore_columns=[], json_columns=[], search_columns=[], max_page_size=100):
        self.db = db
        self.model = model
        self.ignore_columns = ignore_columns
        self.json_columns = json_columns
        self.search_columns = search_columns
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
                current_app.logger.error(str(e))
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
                    current_app.logger.error(str(e))
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
        search = request.args.get('_search')

        query = self.model.query
        for k, v in request.args.items():
            if isinstance(k, str):
                ks = k.split(':')
                if hasattr(self.model, ks[0]):
                    col = getattr(self.model, ks[0])
                    v = self._str_to_date_time(type(col.type), v)
                    if len(ks) > 1:
                        v = None if v == 'null' else v
                        query = self._filter_with_operator(query, col, ks[1], v)
                    else:
                        query = query.filter(col == v)

        query = self._filter_with_search(query, search)
        query = self._filter_with_sort(query, sort, desc)

        total = query.count()
        objs = query.slice((page - 1) * page_size, page * page_size).all()
        ret = {"list": [self._to_dict(o) for o in objs], "page": page, "page_size": page_size, "total": total}
        return self._resp(data=ret)

    def _filter_with_search(self, query, search):
        if search and self.search_columns:
            if self.db.engine.name != 'sqlite':
                # sqlite has no concat function
                cols = []
                for col_name in self.search_columns:
                    if hasattr(self.model, col_name):
                        cols.append(getattr(self.model, col_name))
                if cols:
                    query = query.filter(self.db.func.concat(*cols).contains(search))
        return query

    def _filter_with_sort(self, query, sort, desc):
        if sort and hasattr(self.model, sort):
            if desc and str(desc) == '1':
                query = query.order_by(getattr(self.model, sort).desc())
            else:
                query = query.order_by(getattr(self.model, sort))
        return query

    def _filter_with_operator(self, query, coloumn, operator, value):
        if operator == 'eq':
            query = query.filter(coloumn == value)
        if operator == 'ne':
            query = query.filter(coloumn != value)
        if operator == 'in':
            query = query.filter(coloumn.in_(value.split(',')))
        if operator == 'notin':
            query = query.filter(coloumn.notin_(value.split(',')))
        if operator == 'contains':
            query = query.filter(coloumn.contains(value))
        if operator == 'notcontains':
            query = query.filter(~coloumn.contains(value))
        if operator == 'gt':
            query = query.filter(coloumn > value)
        if operator == 'ge':
            query = query.filter(coloumn >= value)
        if operator == 'lt':
            query = query.filter(coloumn < value)
        if operator == 'le':
            query = query.filter(coloumn <= value)
        return query

    def _to_dict(self, obj):
        ret = {}
        for column in obj.__table__.columns:
            if column.name not in self.ignore_columns:
                value = getattr(obj, column.name)
                if value and column.type.__class__ in [sqltypes.DateTime, sqltypes.Date, sqltypes.Time]:
                    ret[column.name] = str(value)
                elif column.name in self.json_columns:
                    ret[column.name] = self._str_to_json(value)
                else:
                    ret[column.name] = value
        return ret

    def _update_model_from_dict(self, obj, data):
        if obj and data:
            for k, v in data.items():
                if hasattr(obj, k):
                    column_type = type(getattr(obj.__table__.columns, k).type)
                    if column_type in [sqltypes.DateTime, sqltypes.Date, sqltypes.Time]:
                        v = self._str_to_date_time(column_type, v)
                    if column_type == sqltypes.Boolean:
                        if str(v).lower() in ['1', 'true', 'yes']:
                            v = True
                        elif str(v).lower() in ['0', 'false', 'no']:
                            v = False
                        else:
                            v = None
                    if k in self.json_columns:
                        v = self._json_to_str(v)
                    setattr(obj, k, v)
        return obj

    def _str_to_date_time(self, column_type, value):
        if value:
            if column_type == sqltypes.DateTime:
                value = parse(value)
            if column_type == sqltypes.Date:
                value = parse(value).date()
            if column_type == sqltypes.Time:
                value = parse(value).time()
        return value

    def _json_to_str(self, obj):
        if obj and isinstance(obj, dict):
            return json.dumps(obj)
        return obj

    def _str_to_json(self, text):
        result = text
        try:
            result = json.loads(text)
        except:
            result = text
        return result

    def _resp(self, code=200, msg="OK", data={}):
        return jsonify(code=code, msg=msg, data=data), code

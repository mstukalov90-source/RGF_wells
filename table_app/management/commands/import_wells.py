import xlrd
from datetime import datetime
from django.core.management.base import BaseCommand
from table_app.models import Well


HEADER_MAPPING = {
    'Регион': 'region',
    'Месторождение': 'name_mst',
    'Площадь': 'plosh',
    'Номер лицензии': 'n_lic',
    'Название лицензионного участка': 'lic',
    'Номер куста': 'n_kust',
    'Номер Скв.': 'n_skv',
    'Тип скважины': 'tip_skv',
    'Забой (метры)': 'sk_zb',
    'Альтитуда ротора (метры)': 'altit',
    'Давление забоя (Мпа)': 'd_zaboi',
    'Давление пластовое (Мпа)': 'd_plast',
    'Диаметр скважины (мм)': 'd_skv',
    'λ (градусы,минуты,секунды)': 'x',
    'φ (градусы, минуты, секунды)': 'y',
    'Индекс': 'id_strat',
    'Название': 'strat',
    'Абсолютная отметка кровли испытания (метры)': 'abs_o_k',
    'Абсолютная отметка подошвы испытания (метры)': 'abs_o_p',
    'Штутцер (мм)': 'shtucr',
    'Дебит нефти (тонн\сут)': 'debit_n',
    'Плотность нефти (тонн\м3)': 'uvp_n',
    'Дебит воды (тонн\сут)': 'debit_v',
    'Дебит газа (куб.метры\сут)': 'debit_g',
    'Дебит конденсата (тонн\сут)': 'debit_k',
    'Характер насыщения': 'char_nas',
    'Эфективная мощность отложений (метры)': 'm_otl',
    'Дата окончания бурения (д.м.г.)': 'o_rab',
    'ID_XY': 'id_xy',
    'Автор записи': 'auth',
    'Наличие материала': 'material_available',
}


def normalize_header(value):
    if value is None:
        return ''
    value = str(value).strip()
    if value.lower().startswith('unnamed') or value == '':
        return ''
    return value


def normalize_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value or value == '+':
            return None
    return value


def parse_number(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip().replace(',', '.')
        if not value or value == '+':
            return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_date(value, book=None):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        for fmt in ('%d.%m.%Y', '%d.%m.%y', '%Y-%m-%d'):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None
    if isinstance(value, (int, float)) and book is not None:
        try:
            return xlrd.xldate_as_datetime(value, book.datemode).date()
        except xlrd.XLDateError:
            return None
    return None


class Command(BaseCommand):
    help = 'Import well records from an XLS workbook into the Well model'

    def add_arguments(self, parser):
        parser.add_argument('xls_path', nargs='?', default='скв_испытания 300321.xls',
                            help='Path to the XLS file to import')
        parser.add_argument('--truncate', action='store_true',
                            help='Delete existing wells before importing')
        parser.add_argument('--sheet-name', default='скв_пласт',
                            help='Sheet name to read from the workbook')

    def handle(self, *args, **options):
        path = options['xls_path']
        sheet_name = options['sheet_name']
        truncate = options['truncate']

        workbook = xlrd.open_workbook(path)
        try:
            sheet = workbook.sheet_by_name(sheet_name)
        except xlrd.biffh.XLRDError as exc:
            raise ValueError(f'Sheet {sheet_name!r} not found in {path}') from exc

        headers = []
        for col_idx in range(sheet.ncols):
            first_header = normalize_header(sheet.cell_value(0, col_idx))
            second_header = normalize_header(sheet.cell_value(1, col_idx))
            header = first_header or second_header
            if headers and first_header == headers[-1] and second_header:
                header = second_header
            headers.append(header)

        field_map = {
            idx: HEADER_MAPPING.get(name)
            for idx, name in enumerate(headers)
            if HEADER_MAPPING.get(name)
        }

        if truncate:
            self.stdout.write('Deleting existing wells...')
            Well.objects.all().delete()

        imported = 0
        for row_idx in range(2, sheet.nrows):
            raw_row = [sheet.cell(row_idx, col_idx) for col_idx in range(sheet.ncols)]
            data = {}
            for col_idx, model_field in field_map.items():
                if not model_field:
                    continue
                cell = raw_row[col_idx]
                if model_field in ('sk_zb', 'altit', 'd_zaboi', 'd_plast', 'd_skv',
                                   'abs_o_k', 'abs_o_p', 'shtucr', 'debit_n', 'uvp_n',
                                   'debit_v', 'debit_g', 'debit_k', 'm_otl'):
                    value = parse_number(cell.value if hasattr(cell, 'value') else cell)
                elif model_field == 'o_rab':
                    value = parse_date(cell.value if hasattr(cell, 'value') else cell, workbook)
                else:
                    raw_value = cell.value if hasattr(cell, 'value') else cell
                    value = normalize_value(raw_value)
                data[model_field] = value

            Well.objects.create(**data)
            imported += 1
            if imported % 1000 == 0:
                self.stdout.write(f'Imported {imported} rows...')

        self.stdout.write(self.style.SUCCESS(f'Imported {imported} wells from {path}'))

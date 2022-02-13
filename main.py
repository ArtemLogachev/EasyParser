import requests
import re
from datetime import date
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

spreadsheetId = '****************' 

CREDENTIALS_FILE = 'credentials.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API


def read_data(list_name):
    ranges = [list_name]  # TODO: Update placeholder value.

    # How values should be represented in the output.
    # The default render option is ValueRenderOption.FORMATTED_VALUE.
    value_render_option = 'FORMATTED_VALUE'  # TODO: Update placeholder value.

    # How dates, times, and durations should be represented in the output.
    # This is ignored if value_render_option is
    # FORMATTED_VALUE.
    # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
    date_time_render_option = 'SERIAL_NUMBER'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, ranges=ranges,
                                                       valueRenderOption=value_render_option,
                                                       dateTimeRenderOption=date_time_render_option)
    response = request.execute()

    return response['valueRanges'][0]['values']


def write_data(lines, list_name):
    read_list = read_data(list_name)
    data = []
    for i in range(len(lines)):
        if not (lines[i] in read_list):
            data.append(lines[i])
    range_ = list_name
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        'values': data
    }
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=range_,
                                                     valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()


def gis(url, name, saloon):
    res = saloon
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    r = requests.get(url, headers=headers)
    lines = re.findall(r'<span class="_16s5yj36" title=".*?">.*?</span>|<div class="_4mwq3d">.*?</div>', r.text)
    result = [[]]
    count = 0
    j = 0
    for i in range(len(lines)):
        lines[i] = re.sub('<.*?>', '', lines[i])
        lines[i] = re.sub(', отредактировано', '', lines[i])
        if lines[i] == 'сегодня':
            lines[i] = date.today().strftime("%d %B %Y")
            lines[i].replace('September', 'Сентября')
        if count == 2:
            count = 0
            result.append([])
            j += 1
        result[j].append(lines[i])
        count += 1
    for i in range(len(result)):
        result[i].append('2ГИС')
        result[i].append(name)
    res.extend(result)
    return res

saloons_gis_smr = {
    'Name': 'link',
    'Name': 'link',
    'Name': 'link',
    'Name': 'link',
    'Name': 'link',
    }


saloon_g = []
for i in saloons_gis_smr.keys():
    saloon_g = gis(saloons_gis_smr[i], i, saloon_g)

write_data(saloon_g,'List!A1:D')

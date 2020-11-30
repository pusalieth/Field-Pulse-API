#!/usr/bin/python3

import sys, json, cgitb, cgi, database_manager, os, pymongo, pdf_conversion, time, requests, onedrive, urllib, math, datetime, re, pytz
# print(os.getcwd())
# allows for debugging errors from the cgi scripts in the browser
# cgitb.enable()

# handler = {}
# if 'HTTP_COOKIE' in os.environ:
#     cookies = os.environ['HTTP_COOKIE']
#     cookies = cookies.split('; ')

#     for cookie in cookies:
#         cookie = cookie.split('=')
#         handler[cookie[0]] = cookie[1]

# authdb = database_manager.MANAGER()
# self.result = authdb.reAuthUser(
#     handler.get('organization'), handler.get('username'), handler.get('pwdhash'))

class API:
    def __init__(self):
        my_cookies = {
            'DASHBOARD_WIDGETS_LOCAL_STORAGE_KEY': '{"version":"1.0","cache":"{\"widgetsConfigurations\":[\"{\\\"widgetClass\\\":\\\"ServiceDashboardWidget\\\",\\\"order\\\":0,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"CustomerDashboardWidget\\\",\\\"order\\\":1,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"EstimateDashboardWidget\\\",\\\"order\\\":2,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"InvoiceDashboardWidget\\\",\\\"order\\\":3,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"SalesDashboardWidget\\\",\\\"order\\\":4,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"PaymentDashboardWidget\\\",\\\"order\\\":5,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"ProjectDashboardWidget\\\",\\\"order\\\":6,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"TimesheetDashboardWidget\\\",\\\"order\\\":7,\\\"deleted\\\":false}\",\"{\\\"widgetClass\\\":\\\"ServiceMapWidget\\\",\\\"order\\\":8,\\\"deleted\\\":false}\"]}"}',
            'token': '',
            'user_id': ''
        }
        my_headers = {
            'Host': 'sandbox.fieldpulse.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://webapp.fieldpulse.com/',
            'Authorization': 'Bearer %s' % my_cookies['token'],
            'Content-Type': 'application/json',
            'Origin': 'https://webapp.fieldpulse.com',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        # get  https://sandbox.fieldpulse.com:6001/socket.io/?EIO=3&transport=polling&t=NA65fjQ
        # post https://sandbox.fieldpulse.com:6001/socket.io/?EIO=3&transport=polling&t=NA65fpX&sid=MmKRqxHQSOLr91KncP_z

        self.todays_date = datetime.datetime.now(
            pytz.timezone('US/Pacific')).strftime("%B %d, %Y")
        self.main_url = 'https://sandbox.fieldpulse.com/v2.5/'
        self.session = requests.session()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, my_cookies)
        self.session.headers.update(my_headers)
        self.login()

    def login(self):
        login_data = {"email": "",
                      "password": "",
                      "timezone": "America/Phoenix"}
        self.login_session_info = self.getJSON('company')
        if(self.login_session_info['error'] == "token_not_provided"):
            self.postJSON('authorize', data=login_data)
            # print('Logging In...')
            pass
        else:
            # print('Already logged in to Pulse...')
            pass
        # print(self.session.cookies.get_dict())
        # print(self.session.headers)
        # print(self.login_session_info)

    def addCustomer(self, first_name=None, last_name=None, email=None, company_name=None, phone=None, address_1=None, address_2=None, city=None, state=None, account_type=None, zipcode=None, notes=None, customer_data=None):
        if(customer_data == None):
            values = locals()
            del values['self']
            from pulse_customer import customer_data
            customer_data.update(values)

        added_customer_response = self.postJSON(
            'customer', data=json.dumps(customer_data))
        if(added_customer_response != None):
            return added_customer_response

    def fixCustomer(self):
        # https://sandbox.fieldpulse.com/v2.5/customer/{customer_id}
        pass

    def addInvoice(self, customer_id, price, notes=""):
        from pulse_invoice import invoice_data
        invoice_data["customer_id"] = customer_id
        invoice_data["line_items"][0]["line_components"][0]["unit_price"] = price
        invoice_data["notes"] = notes
        added_invoice_response = self.postJSON(
            'invoice', data=json.dumps(invoice_data))
        return added_invoice_response

    def addFile(self, customer_id, file):
        opened_file = {'upload_file': open(file, 'rb')}
        file_size = str(os.path.getsize(file))
        filename, file_extension = os.path.splitext(file)
        file_header = {
            'parent-type': 'customer',
            'parent-id': str(customer_id),
            'file-extension': str(file_extension),
            'Content-Length': str(file_size),
            'display-name': str(filename)
        }
        added_file_response = self.postJSON(
            'file', files=opened_file, headers=file_header)
        return added_file_response

    def addPDF(self, customer_id, pdf_name, pdf_bytes):
        opened_file = {'upload_file': pdf_bytes}
        file_size = str(len(pdf_bytes))
        file_header = {
            'parent-type': 'customer',
            'parent-id': str(customer_id),
            'file-extension': 'pdf',
            'Content-Length': str(file_size),
            'display-name': '%s %s' % (pdf_name, self.todays_date)
        }
        added_file_response = self.postJSON(
            'file', files=opened_file, headers=file_header)
        return added_file_response

    def getCustomerList(self, length, deleted='false', attribute='sort_key', order='asc'):
        # limit=5000 &page=7 &deleted=false &sort[0][attribute]=sort_key &sort[0][order]=asc &sort[1][attribute]=searchable &sort[1][order]=asc
        customer_list = []
        size_limit = int(length / 100) * 100
        page_num = 1
        reverse = False
        # print('Downloading %s pages' % int(length / size_limit))
        while True:
            dict = {
                'limit': str(size_limit),
                'page': str(page_num),
                'deleted': deleted,
                'sort[0][attribute]': attribute,
                'sort[0][order]': order
                # 'sort[1][attribute]': 'searchable',
                # 'sort[1][order]': 'asc'
            }
            server = self.getJSON('customer?', params=dict)
            if(server == None):
                sys.exit()
            elif(not reverse):
                # print('Adding asc order to list')
                for record in list(server['response']):
                    customer_list.append(record)
                order = 'dsc'
                reverse = True
                # print('Reversing order...')
                # print('Total length of customer list %s' % len(customer_list))
            elif(reverse):
                # print('Adding dsc order to list')
                last_asc_customer = customer_list.pop()
                temp_list = []
                for record in list(server['response']):
                    if(last_asc_customer != record):
                        temp_list.append(record)
                    else:
                        temp_list.append(record)
                        break

                temp_list.reverse()
                customer_list = customer_list + temp_list
                break

        return customer_list

    def getJobList(self, customer_id, team_ids=[], limit=20, dynamic_attributes='invoice_status', order='desc'):
        dict = {
            'limit': str(limit),
            'page': '1',
            'deleted': 'false',
            'sort[0][attribute]': 'start_time',
            'sort[0][order]': str(order),
            'dynamic_attributes[0]': str(dynamic_attributes),
            'filter[0][action]': 'where',
            'filter[0][attribute]': 'customer_id',
            'filter[0][operator]': '=',
            'filter[0][value]': str(customer_id),
            'filter[0][class]': 'string'
        }
        for index in range(0, len(team_ids)):
            dict.update({
                'asn[%s][team_id]' % index: str(team_ids[index]),
                'asn[%s][unassigned]' % index: 'true'
            })
        job_list = self.getJSON('job?', params=dict)
        return job_list.get('response')

    def putJobStatus(self, job_id, status):
        job_status = self.putJSON('job/%s' % str(job_id), params={"status": status})
        return job_status.get('response')

    def putJobNotes(self, customer_id, job_id, notes):
        dict = {
            '_id': str(job_id),
            'customer_id': str(customer_id),
            'notes': str(notes)
        }
        notes = self.putJSON('job/%s' % str(job_id), params=dict)
        return notes.get('response')

    def importCustomers(self):
        import_customer_response = self.postJSON(
            'customer/import', data=json.dumps(file_data))
        if(import_customer_response != None):
            return import_customer_response

    def exportCustomers(self):
        export_response = self.postJSON('customer/export-new/email')
        return export_response

    def search4Customer(self, search_terms):
        search_query = ''
        for term in search_terms:
            if(term == search_terms[0]):
                search_query += '(^%s)' % search_terms[0]
            else:
                search_query += '|(^%s)' % term
        dict = {
            'search': str(search_query),
            'limit': '1000'
        }
        search_result_json = self.getJSON('customer?', params=dict)
        # print(search_result_json)
        return search_result_json['response']

    def getCustomerID(self, search_terms):
        search_result_json = self.search4Customer(search_terms)
        # print(search_result_json)
        if(len(search_result_json.get('response')) > 0):
            return search_result_json['response'][0]['_id']
        else:
            return None

    def getCustomer(self, customer_id):
        customer = self.getJSON(
            'customer/%s?deleted=true&rel[parent]=' % customer_id)['response']
        # print(search_result_json)
        return customer

    def deleteCustomer(self, customer_id):
        deleted_customer_response = json.loads(self.session.delete(
            '%scustomer/%s' % (self.main_url, customer_id), timeout=3.0).text)
        return deleted_customer_response

    def getLatestCustomerID(self):
        return self.getLatestCustomerList()['response'][0]

    def getLatestCustomerList(self, length=20, deleted='false', attribute='updated_at', order='desc'):
        dict = {
            'limit': str(length),
            'deleted': str(deleted),
            'sort[0][attribute]': str(attribute),
            'sort[0][order]': str(order)
        }
        customer_list = self.getJSON('customer?', params=dict)
        return customer_list

    def putJSON(self, path, params=None, data=None, files=None, headers=None):
        # print('%s%s' % (self.main_url + path, self.getURL(params)))
        response = self.session.put(url='%s' % (
            self.main_url + path), params=params, timeout=30).text
        try:
            return json.loads(response)
        except Exception as e:
            if('Whoops, looks like something went wrong.' in response):
                # print('Server 500 Error')
                pass
            else:
                # print('Return response from Field Pulse put method failed due to: %s\n%s' % (e, response))
                pass

            return None

    def postJSON(self, path, params=None, data=None, files=None, headers=None):
        try:
            return json.loads(self.session.post(url='%s' % (self.main_url + path), params=params, data=data, files=files, headers=headers, timeout=30).text)
        except Exception as e:
            if('Whoops, looks like something went wrong.' in response):
                # print('Server 500 Error')
                pass
            else:
                # print('Return response from Field Pulse post method failed due to: %s' % e)
                pass
            
            return None

    def getJSON(self, path, params=None, data=None):
        # print('%s%s' % (self.main_url + path, self.getURL(params)))
        response = self.session.get(url='%s' % (
            self.main_url + path), params=params, data=data, timeout=30).text
        try:
            return json.loads(response)
        except Exception as e:
            if('Whoops, looks like something went wrong.' in response):
                # print('Server 500 Error')
                pass
            else:
                # print('Return response from Field Pulse get method failed due to: %s\n%s' % (e, response))
                pass

            return None

    def getURL(self, dict):
        if(dict != None):
            return urllib.parse.urlencode(dict)


if __name__ == "__main__":
    API()

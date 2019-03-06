from locust import HttpLocust, TaskSet, task
import re

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.login()

    #@task(1)
 #   tasks = {login: 2}
    def login(self):
  #      self.client.post("/login",
  #                       {"username":"ellen_key",
  #                        "password":"education"})

        headers = {'SOAPAction': 'web_custom_request'}

        response = self.client.post("/awsi_uams/services/UAMSLoginService",
                             "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ws=\"http://ws.ws.client.uamsimpl.amdocs\">"
                             "   <soapenv:Header/>"
                             "   <soapenv:Body>"
                             "      <ws:loginCall>"
                             "         <!--Optional:-->"
                             "         <ws:in0>ABPBatchUser</ws:in0>"
                             "         <!--Optional:-->"
                             "         <ws:in1>Unix11</ws:in1>"
                             "         <!--Optional:-->"
                             "         <ws:in2>LE_tc01_PE</ws:in2>"
                             "         <!--Optional:-->"
                             "         <ws:in3>CM</ws:in3>"
                             "      </ws:loginCall>"
                             "   </soapenv:Body>"
                             "</soapenv:Envelope>",
                            headers = headers,
                            name = "UAMSLogin",
                      #      catch_response = True
                         )

        abc = str(response.content)
        self.token = (re.search("EXT&lt;(.*);appId",abc)).group(1)
        print("In login "+self.token)
        #self.logout(token)

    def on_stop(self):
        self.logout()

    #@task(1)
    def logout(self):
        headers = {'SOAPAction': 'web_custom_request'}
        print("In logout "+self.token)
        response = self.client.post("/awsi_uams/services/UAMSLoginService",
                                    "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ws=\"http://ws.ws.client.uamsimpl.amdocs\">"
		                            "   <soapenv:Header/>"
		                            "   <soapenv:Body>"
		                            "      <ws:logoutCall>"
		                            "         <!--Optional:-->"
		                            "         <ws:in0>"+self.token+"</ws:in0>"
		                            "      </ws:logoutCall>"
		                            "   </soapenv:Body>"
		                            "</soapenv:Envelope>",
                                    headers=headers,
                                    name="UAMSLogout",
                                    #      catch_response = True
                                    )

        abc = str(response.content)
        print((re.search("<logoutCallReturn>(.*)</logoutCallReturn>", abc)).group(1))

class WebsiteUser(HttpLocust):
   # token = ""
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

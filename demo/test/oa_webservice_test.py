# -*- coding: utf-8 -*-
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
import json
import re

imp = Import("http://localhost/services/RequestService")
imp_javax = Import("http://http.servlet.javax")
imp_util_java = Import("http://util.java")
imp_lang_java = Import("http://lang.java")
imp_servlet_java = Import("http://servlet.javax")
imp_security_java = Import("http://security.java")
imp_io_java = Import("http://io.java")
imp_weaver = Import("http://conn.weaver")
imp_hrm = Import("http://hrm.weaver")
imp_workflow = Import("http://request.workflow.weaver")

doctor = ImportDoctor(imp)
doctor.add(imp_javax, imp_util_java, imp_lang_java, imp_servlet_java, imp_security_java, imp_io_java,
           imp_weaver, imp_hrm, imp_workflow)
test = Client("http://192.168.120.8//services/RequestService?wsdl", doctor=doctor)
# print test
service = test.service
requestResp = service.getRequest(in0=20158)
# print requestResp.requestManager.requestname
# # print requestResp.detailTableInfo.detailTable.DetailTable
# for detail in requestResp.detailTableInfo.detailTable.DetailTable:
#     print detail.id
# line = u'【2917001L】基于高光谱的无人机航摄平台'
# pattern = ur'【(.*?)】'
# matchObj = re.search(pattern, line, re.M | re.I)
# if matchObj:
#     print matchObj.group(1)
# else:
#     print 'not match'

# testfile = open("../test.txt", "w+")
# print >>testfile, requestResp
# testfile.close()
# requestManager = test.factory.create('ns17:RequestManager')
# print requestManager
# requestInfo = test.factory.create('ns16:RequestInfo')
# print requestInfo

# Suds ( https://fedorahosted.org/suds/ )  version: 0.6
#
# Service ( RequestService ) tns="http://localhost/services/RequestService"
#    Prefixes (11)
#       ns0 = "http://conn.weaver"
#       ns11 = "http://hrm.weaver"
#       ns12 = "http://http.servlet.javax"
#       ns13 = "http://io.java"
#       ns14 = "http://lang.java"
#       ns15 = "http://localhost/services/RequestService"
#       ns16 = "http://request.workflow.soa.weaver"
#       ns17 = "http://request.workflow.weaver"
#       ns18 = "http://security.java"
#       ns19 = "http://servlet.javax"
#       ns20 = "http://util.java"
#    Ports (1):
#       (RequestServiceHttpPort)
#          Methods (21):
#             LoadTemplateProp(xs:string in0)
#             createRequest(ns16:RequestInfo in0)
#             deleteRequest(xs:int in0)
#             forwardFlow(xs:int in0, xs:int in1, xs:string in2, xs:string in3, xs:string in4)
#             getHendledRequestBySearch(xs:int in0, xs:string in1, xs:string in2, xs:string in3)
#             getMyRequestBySearch(xs:int in0, xs:string in1, xs:string in2, xs:string in3)
#             getPendingRequestBySearch(xs:int in0, xs:string in1, xs:string in2, xs:string in3)
#             getProcessedRequestBySearch(xs:int in0, xs:string in1, xs:string in2, xs:string in3)
#             getPropValue(xs:string in0, xs:string in1)
#             getRequest(xs:int in0)
#             getRequest1(ns17:RequestManager in0)
#             getRequest2(xs:int in0, xs:int in1)
#             getRequest3(ns17:RequestManager in0, xs:int in1)
#             getRequestLogs(xs:string in0, xs:int in1, xs:int in2)
#             getRightMenu(xs:int in0, xs:int in1, xs:int in2, xs:int in3, xs:int in4, xs:boolean in5)
#             nextNodeByReject(xs:int in0, xs:int in1, xs:string in2)
#             nextNodeBySubmit(ns16:RequestInfo in0, xs:int in1, xs:int in2, xs:string in3)
#             nextNodeBySubmit1(ns16:RequestInfo in0, xs:int in1, xs:int in2, xs:string in3, xs:string in4)
#             whetherMustInputRemark(xs:int in0, xs:int in1, xs:int in2, xs:int in3, xs:int in4)
#             writeLog(xs:anyType in0)
#             writeLog1(xs:string in0, xs:anyType in1)
#          Types (35):
#             ns16:ArrayOfCell
#             ns12:ArrayOfCookie
#             ns16:ArrayOfDetailTable
#             ArrayOfInt
#             ns16:ArrayOfLog
#             ns16:ArrayOfProperty
#             ns16:ArrayOfRequestBase
#             ns16:ArrayOfRow
#             ArrayOfString
#             ns13:BufferedReader
#             ns16:Cell
#             ns12:Cookie
#             ns16:DetailTable
#             ns16:DetailTableInfo
#             ns20:Enumeration
#             ns12:HttpServletRequest
#             ns12:HttpSession
#             ns12:HttpSessionContext
#             ns20:Locale
#             ns16:Log
#             ns16:MainTableInfo
#             ns18:Principal
#             ns16:Property
#             ns0:RecordSetTrans
#             ns16:RequestBase
#             ns16:RequestInfo
#             ns16:RequestLog
#             ns17:RequestManager
#             ns16:Row
#             ns19:ServletContext
#             ns19:ServletInputStream
#             ns14:StringBuffer
#             ns11:User
#             anyType2anyType2anyTypeMapMap
#             anyType2anyTypeMap

"""

Basic Final Project Description
The basic final project for the “Programming in Network Environments” course is the
development of an application for searching and listing drugs and companies inside “drug product
labelling“ using the OpenFDA API: https://api.fda.gov/drug/label.json
In the project all the previous practices will be included and the project must
follow the rules described in this specification so it can be tested automatically

Directory and files for the project
The project must be delivered inside the GitHub “openfda” repository which each
student has already created.
https://github.com/<github-login>/openfda
In this repository a directory with the name “openfda-project” must exists and it
must include the file “server.py” with the implementation of the web server.
The server must be started with “python3 server.py” and this must start the
HTTP web server that must be listening in 8000 port.

Web server API to be implemented
The web server must offer the API:
    searchDrug?active_ingredient=<name>
    searchCompany?company=<company_name>
    listDrugs
    listCompanies
The response for all this end points must be a HTML list (<ul></ul>) with the results.
To pass the automatic tests in the project, the next file must be copied:
https://github.com/acs-test/openfda-project/blob/master/test_openfda.py
inside the “openfda-project” student directory. And to execute the tests:./test_openfda.py

Web server API Details
searchDrug?active_ingredient=<name>
Search drugs that includes <name> in the active_ingredient .
searchCompany?company=<company_name>
Search drugs that includes <company_name> in the openfda.manufacturer_name field.
listDrugs
List drugs returned by default by OpenFDA
listCompanies
List with the openfda.manufacturer_name from the drugs returned by default by OpenFDA. If this field does not exists
it should appear as “Unknown”.

"""

import server

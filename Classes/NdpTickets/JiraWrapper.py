#!/usr/bin/env python
# -*- coding: utf-8 -*-
# current_day = datetime.datetime.now().day
# current_month = datetime.datetime.now().month
# current_year = datetime.datetime.now().year


import datetime
from datetime import timedelta
from Classes.LoggerFile.LogFile import logger
from jira.client import JIRA, JIRAError
import urllib3
from Classes.DataReaders.config_ini import Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class JiraException(Exception):
    pass


class Jira(Config):

    def __init__(self, **kwargs):

        super(Jira, self).__init__()
        self.description = None
        self.issue_aus = None
        self.issue_us = None
        self.issue_uk = None
        self.issue_es = None
        self.issue_de = None
        self.issue_fr = None
        self.issue_apac = None
        self.issue_mea = None

        self.create_aus = None
        self.create_us = None
        self.create_apac = None
        self.create_de = None
        self.create_mea = None
        self.create_fr = None
        self.create_es = None
        self.create_uk = None

        self.options = {
            'server': self.section_value[4],
            'verify': False
        }

        self.client = None

        if len(kwargs) != 2:
            raise JiraException(
                'In order to use this class you need to specify a user and a password as keyword arguments!')
        else:
            if 'username' in kwargs.keys():
                self.username = kwargs['username']
            else:
                raise JiraException('You need to specify a username as keyword argument!')
            if 'password' in kwargs.keys():
                self.password = kwargs['password']
            else:
                raise JiraException('You need to specify a password as keyword argument!')

            try:
                self.client = JIRA(self.options, basic_auth=(self.username, self.password))
            except Exception:
                raise JiraException('Could not connect to the API, invalid username or password!')

    def get_projects(self, raw=False):

        projects = []
        for project in self.client.projects():
            if raw:
                projects.append(project)
            else:
                projects.append({'Name': str(project.key), 'Description': str(project.name)})
        return projects

    @staticmethod
    def date_create():
        my_date = datetime.datetime.now().date()
        return my_date

    @staticmethod
    def sixth_day():
        now = datetime.datetime.now().date()
        start_month = datetime.datetime(now.year, now.month, 1)
        date_on_next_month = start_month + datetime.timedelta(35)
        start_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
        last_day_month = start_next_month - datetime.timedelta(1)
        sixth_day_month = last_day_month.date() + timedelta(6)
        return sixth_day_month

    def issue_description(self):

        description = "Hi Team" + "\n" + "Hope you are doing well" + "\n" + \
                      "Kindly confirm the current advertisers and accounts from the PDF attached." + "\n" + \
                      "Making sure that for each platform the correct account id, advertiser or account name get" + \
                      "\n" + "included in the NDP data for ALL channels." + "\n" + \
                      "Note: Do let us know if there is any account that needs to be removed." + "\n" + \
                      "Please make sure that the media plan is uploaded on the NeoSageCentral SharePoint Folder." \
                      + "\n" \
                      + "https://insidemedia.sharepoint.com/sites/neosagecentral/Shared%20Documents/" \
                        "Forms/AllItems.aspx?id=%2Fsites%2Fneosagecentral%2FShared%20Documents%2FFY18%20Media%" \
                        "20Plans%2FQ4%20Media%20Plans" + "\n" + "Thanks," + "\n" + "Nikita"

        self.description = description

    def de(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma',
                 'nikita.borah', 'deepak.garg', 'mohammad.dilshad',
                 'jennifer.marquez', 'ajaysingh.yadav', 'Ing-y.Chenn', 'anastasia.lanina', 'thilo.babel1']
        assignees = 'anastasia.lanina'
        attachment = [self.section_value[3] + 'DE.xlsx']

        try:
            self.issue_de = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'Test', # 'NDP Data Audit {} DE'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'DE'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            create_de = self.client.create_issue(fields=self.issue_de, prefetch=True)
            self.create_de = create_de

            for j in attachment:
                self.client.add_attachment(self.create_de.id, j)

            for i in watch:
                self.client.add_watcher(self.create_de.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def fr(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma', 'nikita.borah',
                 'deepak.garg', 'mohammad.dilshad', 'jennifer.marquez',
                 'ajaysingh.yadav', 'Maxime.Sarrazin', 'philippine.gurs', 'manon.mercier']
        assignees = 'manon.mercier'
        attachment = [self.section_value[3] + 'FR.xlsx']

        try:
            self.issue_fr = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} FR'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'FR'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_fr = self.client.create_issue(fields=self.issue_fr, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_fr.id, j)

            for i in watch:
                self.client.add_watcher(self.create_fr.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def es(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma',
                 'nikita.borah', 'deepak.garg', 'mohammad.dilshad',
                 'jennifer.marquez', 'ajaysingh.yadav', 'silvia.orofino', 'carmen.candela', 'raquel.hernandez']
        assignees = 'silvia.orofino'
        attachment = [self.section_value[3] + 'ES.xlsx', self.section_value[3] + 'PT.xlsx']

        try:
            self.issue_es = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} ES'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'ES'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_es = self.client.create_issue(fields=self.issue_es, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_es.id, j)

            for i in watch:
                self.client.add_watcher(self.create_es.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def us(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma', 'nikita.borah',
                 'deepak.garg', 'mohammad.dilshad', 'jennifer.marquez', 'ajaysingh.yadav',
                 'vanessa.ezeta']
        assignees = 'vanessa.ezeta'
        attachment = [self.section_value[3] + 'CA.xlsx', self.section_value[3] + 'US.xlsx',
                      self.section_value[3] + 'US & CA.xlsx']

        try:
            self.issue_us = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} US'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'US'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_us = self.client.create_issue(fields=self.issue_us, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_us.id, j)

            for i in watch:
                self.client.add_watcher(self.create_us.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def uk(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma', 'nikita.borah',
                 'deepak.garg', 'mohammad.dilshad', 'jennifer.marquez',
                 'ajaysingh.yadav', 'aman.mastana', 'manon.leymat', 'james.hill', 'alex.ooi', 'sophie.corcinos',
                 'mireia.nadal', 'nick.gardiner']
        assignees = 'manon.leymat'
        attachment = [self.section_value[3] + 'UK.xlsx', self.section_value[3] + 'IE.xlsx']

        try:
            self.issue_uk = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} UK'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'UK'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_uk = self.client.create_issue(fields=self.issue_uk, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_uk.id, j)

            for i in watch:
                self.client.add_watcher(self.create_uk.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    # Done
    def mea(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma',
                 'nikita.borah', 'deepak.garg', 'mohammad.dilshad', 'jennifer.marquez', 'ajaysingh.yadav',
                 'marthinus.matthee', 'Brunette Nkuna']
        assignees = 'gareth.macgregor'
        attachment = [self.section_value[3] + 'ZA.xlsx']

        try:
            self.issue_mea = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} MEA'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'MEA'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_mea = self.client.create_issue(fields=self.issue_mea, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_mea.id, j)

            for i in watch:
                self.client.add_watcher(self.create_mea.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def aus(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma',
                 'nikita.borah', 'deepak.garg', 'mohammad.dilshad',
                 'jennifer.marquez', 'ajaysingh.yadav', 'jon.windred', 'corinne.hewlett']
        assignees = 'corinne.hewlett'
        attachment = [self.section_value[3] + 'AUS.xlsx']

        try:
            self.issue_aus = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} AUS'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'AUS'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_aus = self.client.create_issue(fields=self.issue_aus, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_aus.id, j)

            for i in watch:
                self.client.add_watcher(self.create_aus.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def apac(self):
        watch = ['Dharmendra.mishra', 'ankit.singhal', 'ubaidullah.arifshah', 'ayush.sharma', 'nikita.borah',
                 'deepak.garg', 'mohammad.dilshad', 'jennifer.marquez',
                 'ajaysingh.yadav', 'ravi.chettiar']
        assignees = 'ravi.chettiar'
        attachment = [self.section_value[3] + 'HK.xlsx', self.section_value[3] + 'ID.xlsx',
                      self.section_value[3] + 'MY.xlsx', self.section_value[3] + 'SG.xlsx',
                      self.section_value[3] + 'TH.xlsx']

        try:
            self.issue_apac = {
                'project': {'key': 'MOS'},
                'issuetype': {'name': 'Reporting'},
                'summary': 'NDP Data Audit {} APAC'.format(Jira.date_create().strftime('%B')),
                'description': self.description,
                'customfield_10038': {'value': 'APAC'},
                'customfield_10052': {'value': 'Ad hoc'},
                'customfield_10053': {'value': 'Monthly'},
                "assignee": {
                    "name": assignees
                }, 'duedate': str(Jira.sixth_day())}

            self.create_apac = self.client.create_issue(fields=self.issue_apac, prefetch=True)

            for j in attachment:
                self.client.add_attachment(self.create_apac.id, j)

            for i in watch:
                self.client.add_watcher(self.create_apac.id, i)

        except JIRAError as e:
            logger.error(str(e))
            pass

    def main(self):
        self.get_projects()
        logger.info('reading issue Description' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.issue_description()
        logger.info('Done!reading issue Description' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for DE' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.de()
        logger.info('Done!creating issue for DE' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for FR' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.fr()
        logger.info('Done!creating issue for FR' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for ES' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.es()
        logger.info('Done!creating issue for ES' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for US' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.us()
        logger.info('Done!creating issue for US' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for UK' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.uk()
        logger.info('Done!creating issue for UK' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for MEA' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.mea()
        logger.info('Done!creating issue for MEA' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for AUS' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.aus()
        logger.info('Done!creating issue for AUS' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info('Start!creating issue for APAC' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.apac()
        logger.info('Done!creating issue for APAC' + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))


if __name__ == "__main__":
    MyJira = Jira(username='Dharmendra.mishra@neomediaworld.com', password='yNbGwGbfJwEhI1d56WlG21B1')
    MyJira.main()